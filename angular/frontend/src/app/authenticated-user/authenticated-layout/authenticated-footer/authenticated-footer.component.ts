import { Component } from '@angular/core';
import { AuthService } from '../../../authentication/auth.service';

@Component({
  selector: 'app-authenticated-footer',
  standalone: false,
  templateUrl: './authenticated-footer.component.html',
  styleUrl: './authenticated-footer.component.css'
})
export class AuthenticatedFooterComponent {
  constructor(private authService: AuthService){}

  onLogout(): void {
    this.authService.logout();
  }
}
