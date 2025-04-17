import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { single,  } from 'rxjs';

import { AccountingService } from '../../accounting-service/accounting.service';
import { 
  FreelanceTuitionTransactionRecordModel 
} from 'src/app/models/accounting.model';

@Component({
  selector: 'app-freelance-payments-and-refunds',
  templateUrl: './freelance-payments-and-refunds.component.html',
  styleUrls: ['./freelance-payments-and-refunds.component.css']
})
export class FreelancePaymentsAndRefundsComponent implements OnInit {


  errorMessage: string|undefined = undefined;
  fetchingInProgress:boolean = false;
  freelanceTransactions: FreelanceTuitionTransactionRecordModel[] | undefined = undefined;
  monthFromRouteData:number;
  yearFromRouteData:number;
  total:string = "0";

  constructor(
    private accountingService: AccountingService,
    private route: ActivatedRoute,

  ) { }

  ngOnInit(): void {
    this.monthFromRouteData = +this.route.snapshot.params['month'];
    this.yearFromRouteData = +this.route.snapshot.params['year'];
    this.fetchingInProgress = true;
    this.accountingService.fetchFreelancePaymentsByMonthAndYear(
      this.monthFromRouteData, this.yearFromRouteData
    ).pipe(single()
      ).subscribe({
        next: (res) => { 
          this.freelanceTransactions = res; 
          this.fetchingInProgress = false;
          this.total = this.calculateTotalEarnings(this.freelanceTransactions)
        },
        error: (err) => {
          this.errorMessage = 'There was an error fetching the transactions';
          this.fetchingInProgress = false;
          if (err["detail"]) {
            this.errorMessage = err["detail"];
          }
        }
      }
    );
  }

  calculateTotalEarnings(monthlyBillings: FreelanceTuitionTransactionRecordModel[]) {
    console.log("***************************************")
    let value = 0;
    for (var i = 0; i < monthlyBillings.length; i++) {
      let transaction = monthlyBillings[i]
      if (transaction.transaction_type === "payment") {
        value += transaction.transaction_amount
        console.log(`Payment: ${value}`)
      } else if (transaction.transaction_type === "refund"){
        value -= transaction.transaction_amount
        console.log(`Refund: ${value}`)
      }
    }
    console.log(`Total value: ${value}`)
    console.log("***************************************")
    return this.formatThousand(value);
  }

  onClearErrorMessage() {
    this.errorMessage = undefined;
  }

  formatThousand(value: number): string {
    if (!value) return ''
    let strValue = value.toString()
    return strValue.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
  }


}
