import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms'
import { single, map } from 'rxjs';

import { AccountingService } from '../../accounting-service/accounting.service';
import { 
  FreelanceTuitionTransactionRecordModel 
} from 'src/app/models/accounting.model';
import { monthsAndIntegers, getYearsOptions } from 'src/app/shared-utils/date-time.util';

@Component({
  selector: 'app-freelance-payments-and-refunds',
  templateUrl: './freelance-payments-and-refunds.component.html',
  styleUrls: ['./freelance-payments-and-refunds.component.css']
})
export class FreelancePaymentsAndRefundsComponent implements OnInit {


  errorMessage: string|undefined = undefined;
  fetchingInProgress:boolean = false;
  freelanceTransactions: FreelanceTuitionTransactionRecordModel[] | undefined = undefined;
  readonly monthsAndIntegers:[string, number][] = monthsAndIntegers;
  selectedMonth: [string, number] = ['January', 1];
  selectedYear: number = 2025;
  showMonthlySelectForm: boolean = true;
  total:string = "0";
  years: number[];

  constructor(
    private accountingService: AccountingService
  ) { }

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

  formatThousand(value: number): string {
    if (!value) return ''
    let strValue = value.toString()
    return strValue.replace(/\B(?<!\.\d*)(?=(\d{3})+(?!\d))/g, ",");
  }

  ngOnInit(): void {
    this.years = getYearsOptions();
  }

  onMonthYearSelect(form: NgForm) {
    if (form.invalid) {
      return;
    }
    this.showMonthlySelectForm = false;
    this.selectedYear = form.value.year;
    this.selectedMonth = this.monthsAndIntegers[+form.value.month - 1]
    this.fetchingInProgress = true;
    this.accountingService.fetchFreelancePaymentsByMonthAndYear(
      +form.value.month, +form.value.year
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
          this.showMonthlySelectForm = true;
        }
      }
    );
  }

  showMonthlySelect() {
    this.showMonthlySelectForm = true;
    this.freelanceTransactions = undefined;
  }

}
