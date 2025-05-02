import { Component, Input } from '@angular/core';
import { SchoolModel } from 'src/app/models/school.model';
import { NgForm } from '@angular/forms';
import { Router } from "@angular/router";


@Component({
  selector: 'app-select-date-range-and-school-form',
  standalone: false,
  templateUrl: './select-date-range-and-school-form.component.html',
  styleUrl: './select-date-range-and-school-form.component.css'
})
export class SelectDateRangeAndSchoolFormComponent {

  dateModel1 = Date;
  dateModel2 = Date;
  @Input() schools: SchoolModel[];
  
  constructor(
    private router: Router,
  ) {}

  onNavigateToSchoolReportWithinDateRange(form: NgForm): void {
    if (form.invalid) {
      form.reset();
      return;
    }
    let start_date = `${form.value.date1.year}-${form.value.date1.month}-${form.value.date1.day}`
    let finish_date = `${form.value.date2.year}-${form.value.date2.month}-${form.value.date2.day}`
    const school_id = +form.value.school;
    console.log(`This is the date range: ${start_date} to ${finish_date}`)
    this.router.navigate(
      [
        'authenticated-user', 'scheduling', 'accounting', 
        'school-accounting-report-within-date-range',   
        start_date, finish_date, school_id
      ]
    );
  }


}
