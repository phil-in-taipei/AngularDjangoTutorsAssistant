import { Component, OnInit } from '@angular/core';
import { single } from 'rxjs';
import { ActivatedRoute } from "@angular/router";
import { SchoolAccountingReportModel } from 'src/app/models/accounting.model';

import { AccountingService } from '../../accounting-service/accounting.service';


@Component({
  selector: 'app-school-accounting-report-within-date-range',
  standalone: false,
  templateUrl: './school-accounting-report-within-date-range.component.html',
  styleUrl: './school-accounting-report-within-date-range.component.css'
})
export class SchoolAccountingReportWithinDateRangeComponent {


  errorMessage: string|undefined = undefined;
  fetchingReportInProgress:boolean = true;
  startDateFromRouteData:string;
  finishDateFromRouteData:string;
  schoolIdFromRouteData:number;
  schoolAccountingReport: SchoolAccountingReportModel|undefined = undefined;

  constructor(
    private route: ActivatedRoute,
    private accountingService: AccountingService
  ) { }

  onClearErrorMessage() {
    this.errorMessage = undefined;
  }

  ngOnInit(): void {
    this.startDateFromRouteData = this.route.snapshot.params['start_date'];
    this.finishDateFromRouteData = this.route.snapshot.params['finish_date'];
    this.schoolIdFromRouteData = +this.route.snapshot.params['school_id'];
    this.accountingService.fetchSchoolAccountingReportWithinDateRange(
      this.startDateFromRouteData,
      this.finishDateFromRouteData,
      this.schoolIdFromRouteData
    ).pipe(single()
      ).subscribe({
        next: (res) => { 
          this.schoolAccountingReport = res; 
          this.fetchingReportInProgress = false;
        },
        error: (err) => {
          this.errorMessage = 'There was an error fetching the report';
          this.fetchingReportInProgress = false;
          if (err["detail"]) {
            this.errorMessage = err["detail"];
          }
        }
      }
    );
  }

}
