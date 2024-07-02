import { Component } from '@angular/core';
import { 
  UnauthenticatedHeaderComponent 
} from '../unauthenticated-layout/unauthenticated-header/unauthenticated-header.component';
import { 
  UnauthenticatedFooterComponent 
} from '../unauthenticated-layout/unauthenticated-footer/unauthenticated-footer.component';

@Component({
  selector: 'app-information',
  standalone: true,
  imports: [
    UnauthenticatedFooterComponent,
    UnauthenticatedHeaderComponent
  ],
  templateUrl: './information.component.html',
  styleUrl: './information.component.css'
})
export class InformationComponent {

}
