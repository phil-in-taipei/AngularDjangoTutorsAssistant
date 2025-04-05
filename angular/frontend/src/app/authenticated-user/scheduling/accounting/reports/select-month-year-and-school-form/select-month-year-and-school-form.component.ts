import { Component, Input, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

import { SchoolModel } from 'src/app/models/school.model';

import { 
  monthsAndIntegers, getYearsOptions 
} from 'src/app/shared-utils/date-time.util';

@Component({
  selector: 'app-select-month-year-and-school-form',
  standalone: false,
  templateUrl: './select-month-year-and-school-form.component.html',
  styleUrl: './select-month-year-and-school-form.component.css'
})
export class SelectMonthYearAndSchoolFormComponent implements OnInit{

  years: number[];

  readonly monthsAndIntegers = monthsAndIntegers;

  @Input() schools: SchoolModel[];

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.years = getYearsOptions();
  }


  onNavigateToMonthlyReport(form: NgForm) {
    console.log(form.value);
    if (form.invalid) {
      return;
    }
    const school_id = +form.value.school;
    const month = form.value.month;
    const year = form.value.year;
    if (school_id === 0) {
      this.router.navigate(
        ['/', 'authenticated-user', 'scheduling', 'accounting', 'overall-monthly-accounting-report', month, year],
      );
    } else {
      this.router.navigate(
        ['/', 'authenticated-user', 'scheduling', 'accounting', 'monthly-school-accounting-report', month, year, school_id],
      );
    }
   

  }


}
