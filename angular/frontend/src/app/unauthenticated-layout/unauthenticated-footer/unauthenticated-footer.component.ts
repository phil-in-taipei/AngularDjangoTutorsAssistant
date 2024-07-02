import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';


@Component({
  selector: 'app-unauthenticated-footer',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './unauthenticated-footer.component.html',
  styleUrl: './unauthenticated-footer.component.css'
})
export class UnauthenticatedFooterComponent {

}
