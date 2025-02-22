import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

import { getYearsOptions, monthsAndIntegers } from 'src/app/shared-utils/date-time.util';

@Component({
  selector: 'app-select-month-and-year',
  standalone: false,
  templateUrl: './select-month-and-year.component.html',
  styleUrl: './select-month-and-year.component.css'
})
export class SelectMonthAndYearComponent implements OnInit {

  years: number[];

  readonly monthsAndIntegers = monthsAndIntegers;

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.years = getYearsOptions();
  }


  onMonthAndYearNav(form: NgForm) {
    console.log(form.value);
    if (form.invalid) {
      return;
    }
    const month = form.value.month;
    const year = form.value.year;
    this.router.navigate(
      ['/', 'authenticated-user', 'scheduling', 'recurring-schedule', 'applied-monthly', month, year],
    );

  }


}
