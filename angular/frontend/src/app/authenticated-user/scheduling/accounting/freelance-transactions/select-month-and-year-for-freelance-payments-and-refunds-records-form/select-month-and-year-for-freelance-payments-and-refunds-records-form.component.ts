import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

import { 
  monthsAndIntegers, getYearsOptions 
} from 'src/app/shared-utils/date-time.util';

@Component({
  selector: 'app-select-month-and-year-for-freelance-payments-and-refunds-records-form',
  standalone: false,
  templateUrl: './select-month-and-year-for-freelance-payments-and-refunds-records-form.component.html',
  styleUrl: './select-month-and-year-for-freelance-payments-and-refunds-records-form.component.css'
})
export class SelectMonthAndYearForFreelancePaymentsAndRefundsRecordsFormComponent implements OnInit {

  years: number[];

  readonly monthsAndIntegers = monthsAndIntegers;

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.years = getYearsOptions();
  }

  onNavigateToMonthlyPaymentsandRefundsRecord(form: NgForm) {
    console.log(form.value);
    if (form.invalid) {
      form.reset()
      return;
    }
    const month = form.value.month;
    const year = form.value.year;

    this.router.navigate(
      ['/', 'authenticated-user', 'scheduling', 'accounting', 'monthly-freelance-transactions', month, year],
    );

  }

}
