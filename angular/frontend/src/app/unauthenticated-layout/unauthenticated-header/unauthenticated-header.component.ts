import { Component } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';


@Component({
  selector: 'app-unauthenticated-header',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './unauthenticated-header.component.html',
  styleUrl: './unauthenticated-header.component.css'
})
export class UnauthenticatedHeaderComponent {

}
