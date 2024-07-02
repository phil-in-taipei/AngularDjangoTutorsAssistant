import { Component } from '@angular/core';
import { AuthService } from '../../../authentication/auth.service';

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
}
