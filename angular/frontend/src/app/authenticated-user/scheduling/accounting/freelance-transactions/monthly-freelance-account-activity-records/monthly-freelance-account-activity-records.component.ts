import { Component, OnInit } from '@angular/core';
import { single } from 'rxjs';
import { ActivatedRoute } from "@angular/router";

import { AccountingService } from '../../accounting-service/accounting.service';
import { 
  PurchasedHoursModificationRecordModel 
} from 'src/app/models/accounting.model';

@Component({
  selector: 'app-monthly-freelance-account-activity-records',
  standalone: false,
  templateUrl: './monthly-freelance-account-activity-records.component.html',
  styleUrl: './monthly-freelance-account-activity-records.component.css'
})
export class MonthlyFreelanceAccountActivityRecordsComponent {

  errorMessage: string|undefined = undefined;
  fetchingReportInProgress:boolean = true;
  freelanceAccountIdFromRouteData:number;
  monthFromRouteData:number;
  yearFromRouteData:number;
  monthlyPurchasedHoursModifications: PurchasedHoursModificationRecordModel[]|undefined = undefined;

  constructor(
    private route: ActivatedRoute,
    private accountingService: AccountingService
  ) { }

  onClearErrorMessage() {
    this.errorMessage = undefined;
  }

  ngOnInit(): void {
    this.monthFromRouteData = +this.route.snapshot.params['month'];
    this.yearFromRouteData = +this.route.snapshot.params['year'];
    this.freelanceAccountIdFromRouteData = +this.route.snapshot.params['account_id'];
    this.accountingService.fetchPurchasedHoursModificationRecordsByMonthAndYear(
      this.monthFromRouteData,
      this.yearFromRouteData,
      this.freelanceAccountIdFromRouteData
    ).pipe(single()
      ).subscribe({
        next: (res) => { 
          this.monthlyPurchasedHoursModifications = res; 
          this.fetchingReportInProgress = false;
        },
        error: (err) => {
          this.errorMessage = 'There was an error fetching the records';
          this.fetchingReportInProgress = false;
          if (err["detail"]) {
            this.errorMessage = err["detail"];
          }
        }
      });
  }

}
