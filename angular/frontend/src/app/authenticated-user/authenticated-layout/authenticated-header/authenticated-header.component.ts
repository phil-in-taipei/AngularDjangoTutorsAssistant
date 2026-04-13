import { Component } from '@angular/core';
import { AuthService } from '../../../authentication/auth.service';

declare const bootstrap: any;

@Component({
  selector: 'app-authenticated-header',
  standalone: false,
  templateUrl: './authenticated-header.component.html',
  styleUrl: './authenticated-header.component.css'
})
export class AuthenticatedHeaderComponent {

  constructor(private authService: AuthService) {}


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
