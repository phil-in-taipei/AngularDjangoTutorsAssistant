import { Component, ViewChild } from '@angular/core';
import { AuthService } from '../../../authentication/auth.service';
import { NgbDateStruct, NgbInputDatepicker } from '@ng-bootstrap/ng-bootstrap';
import { Router } from '@angular/router';
import { getDateString } from 'src/app/shared-utils/date-time.util';



declare const bootstrap: any;

@Component({
  selector: 'app-authenticated-header',
  standalone: false,
  templateUrl: './authenticated-header.component.html',
  styleUrl: './authenticated-header.component.css'
})
export class AuthenticatedHeaderComponent {

  searchMode = false;
  dateModel: NgbDateStruct | null = this.todayStruct();

  @ViewChild('d') datepicker?: NgbInputDatepicker;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  private todayStruct(): NgbDateStruct {
    const now = new Date();
    return {
      year: now.getFullYear(),
      month: now.getMonth() + 1,
      day: now.getDate()
    };
  }

  onSearchClick(): void {
    if (!this.searchMode) {
      this.searchMode = true;
      this.dateModel = this.todayStruct();
      // Wait for *ngIf to render the input, then open the calendar
      setTimeout(() => this.datepicker?.open());
      return;
    }
    this.navToSelectedDate();
  }

  navToSelectedDate(): void {
    if (!this.dateModel) { return; }
    const dateString = getDateString(
      this.dateModel.day,
      this.dateModel.month,
      this.dateModel.year
    );
    this.router.navigate(
      ['authenticated-user', 'scheduling', 'schedule-daily', dateString]
    );
    this.exitSearchMode();
  }

  exitSearchMode(): void {
    this.datepicker?.close();
    this.searchMode = false;
  }

  onLogout() {
    this.authService.logout();
  }

  closeNavbar() {
    const collapseElement = document.getElementById('navbarSupportedContent');
    if (collapseElement) {
      const bsCollapse = new bootstrap.Collapse(collapseElement);
      bsCollapse.hide();
    }
  }
}
