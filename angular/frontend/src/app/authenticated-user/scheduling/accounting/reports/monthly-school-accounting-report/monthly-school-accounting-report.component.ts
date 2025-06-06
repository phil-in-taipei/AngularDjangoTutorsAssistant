import { Component, OnInit } from '@angular/core';
import { single } from 'rxjs';
import { ActivatedRoute } from "@angular/router";
import { SchoolAccountingReportModel } from 'src/app/models/accounting.model';

import { AccountingService } from '../../accounting-service/accounting.service';

@Component({
  selector: 'app-monthly-school-accounting-report',
  standalone: false,
  templateUrl: './monthly-school-accounting-report.component.html',
  styleUrl: './monthly-school-accounting-report.component.css'
})
export class MonthlySchoolAccountingReportComponent implements OnInit {

  errorMessage: string|undefined = undefined;
  fetchingReportInProgress:boolean = true;
  monthFromRouteData:number;
  yearFromRouteData:number;
  schoolIdFromRouteData:number;
  schoolMonthlyAccountingReport: SchoolAccountingReportModel|undefined = undefined;

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
    this.schoolIdFromRouteData = +this.route.snapshot.params['school_id'];
    this.accountingService.fetchSchoolAccountingReportByMonthAndYear(
      this.monthFromRouteData,
      this.yearFromRouteData,
      this.schoolIdFromRouteData
    ).pipe(single()
      ).subscribe({
        next: (res) => { 
          this.schoolMonthlyAccountingReport = res; 
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
