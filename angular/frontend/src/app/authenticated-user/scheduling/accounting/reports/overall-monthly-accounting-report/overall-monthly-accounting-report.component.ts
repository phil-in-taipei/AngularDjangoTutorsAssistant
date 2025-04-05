import { Component, OnInit } from '@angular/core';
import { single } from 'rxjs';
import { ActivatedRoute } from "@angular/router";

import { AccountingService } from '../../accounting-service/accounting.service';
import { 
  SchoolsAndFreelanceStudentsAccountingReportModel
 } from 'src/app/models/accounting.model';

@Component({
  selector: 'app-overall-monthly-accounting-report',
  standalone: false,
  templateUrl: './overall-monthly-accounting-report.component.html',
  styleUrl: './overall-monthly-accounting-report.component.css'
})
export class OverallMonthlyAccountingReportComponent {

    errorMessage: string|undefined = undefined;
    fetchingReportInProgress:boolean = true;
    monthFromRouteData:number;
    yearFromRouteData:number;
    monthlyAccountingReport: SchoolsAndFreelanceStudentsAccountingReportModel|undefined = undefined;

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
      this.accountingService.fetchSchoolsAndFreelanceStudentsAccountingReportByMonthAndYear(
        this.monthFromRouteData,
        this.yearFromRouteData,
      ).pipe(single()
        ).subscribe({
          next: (res) => { 
            this.monthlyAccountingReport = res; 
            this.fetchingReportInProgress = false;
          },
          error: (err) => {
            this.errorMessage = 'There was an error fetching the report';
            this.fetchingReportInProgress = false;
            if (err["detail"]) {
              this.errorMessage = err["detail"];
            }
          }
        });
    }
  
}
