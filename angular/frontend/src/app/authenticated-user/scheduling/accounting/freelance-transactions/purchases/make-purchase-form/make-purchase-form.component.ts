import { Component, Input } from '@angular/core';
import { NgForm } from '@angular/forms';

import { AccountingService } from '../../../accounting-service/accounting.service';
import { 
  FreelanceTuitionTransactionModel, FreelanceTuitionTransactionRecordModel 
} from 'src/app/models/accounting.model';
import { StudentOrClassModel } from 'src/app/models/student-or-class.model';


@Component({
  selector: 'app-make-purchase-form',
  standalone: false,
  templateUrl: './make-purchase-form.component.html',
  styleUrl: './make-purchase-form.component.css'
})
export class MakePurchaseFormComponent {

  errorMessage: string | undefined = undefined;
  @Input() freelanceStudents: StudentOrClassModel[];
  freelanceTuitionTransactionResponse: FreelanceTuitionTransactionRecordModel | undefined = undefined;
  sucessMessage: string | undefined = undefined;

  constructor(private accountingService: AccountingService) { }

}
