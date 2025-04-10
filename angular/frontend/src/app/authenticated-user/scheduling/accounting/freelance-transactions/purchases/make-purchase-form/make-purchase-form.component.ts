import { Component, Input } from '@angular/core';
import { NgForm } from '@angular/forms';
import { single } from 'rxjs';

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
  fetchingInProgress: boolean = false;
  freelanceTuitionTransactionResponse: FreelanceTuitionTransactionRecordModel | undefined = undefined;
  showForm: boolean = true;
  sucessMessage: string | undefined = undefined;

  constructor(private accountingService: AccountingService) { }

  onSubmitPurchase(form: NgForm) {
    if (form.invalid) {
      form.reset();
      return;
    }
    let submissionForm: FreelanceTuitionTransactionModel = {
      transaction_type: "purchase", 
      class_hours_purchased_or_refunded: +form.value.class_hours_purchased_or_refunded,
      student_or_class: +form.value.student_or_class
    }
    this.accountingService.submitFreelanceTuitionTransaction(
      submissionForm
    ).pipe(single()
      ).subscribe({
        next: (res) => { 
          this.freelanceTuitionTransactionResponse = res; 
          this.fetchingInProgress = false;
          this.showForm = false;
        },
        error: (err) => {
          this.errorMessage = 'There was an error submitting the transactions';
          this.fetchingInProgress = false;
          if (err["message"]) {
            this.errorMessage = err["message"];
          }
          this.showForm = true;
        }
      }
    );
  }
}
