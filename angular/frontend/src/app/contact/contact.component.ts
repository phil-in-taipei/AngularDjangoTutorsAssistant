import { Component } from '@angular/core';
import { 
  UnauthenticatedHeaderComponent 
} from '../unauthenticated-layout/unauthenticated-header/unauthenticated-header.component';
import { 
  UnauthenticatedFooterComponent 
} from '../unauthenticated-layout/unauthenticated-footer/unauthenticated-footer.component';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [
    UnauthenticatedFooterComponent,
    UnauthenticatedHeaderComponent
  ],
  templateUrl: './contact.component.html',
  styleUrl: './contact.component.css'
})
export class ContactComponent {

}
