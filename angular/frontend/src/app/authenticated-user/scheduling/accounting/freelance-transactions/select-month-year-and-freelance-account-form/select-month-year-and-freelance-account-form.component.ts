import { Component, Input, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

import { StudentOrClassModel } from 'src/app/models/student-or-class.model';
import { 
  monthsAndIntegers, getYearsOptions 
} from 'src/app/shared-utils/date-time.util';

@Component({
  selector: 'app-select-month-year-and-freelance-account-form',
  standalone: false,
  templateUrl: './select-month-year-and-freelance-account-form.component.html',
  styleUrl: './select-month-year-and-freelance-account-form.component.css'
})
export class SelectMonthYearAndFreelanceAccountFormComponent implements OnInit {

  years: number[];

  readonly monthsAndIntegers = monthsAndIntegers;

  @Input() freelanceAccounts: StudentOrClassModel[];

  constructor(private router: Router) { }

  ngOnInit(): void {
    this.years = getYearsOptions();
  }

  onNavigateToFreelanceAccountActivityRecord(form: NgForm) {
    if (form.invalid) {
      return;
    }
    const account_id = +form.value.account;
    const month = form.value.month;
    const year = form.value.year;

    this.router.navigate(
      ['/', 'authenticated-user', 'scheduling', 'accounting', 'monthly-freelance-account-activity', month, year, account_id],
    );

  }


}
