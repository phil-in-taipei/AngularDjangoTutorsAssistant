import { DeletionResponse } from 'src/app/models/deletion-response';
import { SchoolCreateAndEditModel, SchoolModel } from 'src/app/models/school.model';

export const schoolData: SchoolModel = {
  id: 1,
  school_name: 'Test Elementary School',
  address_line_1: '123 Main Street',
  address_line_2: 'Suite 100',
  contact_phone: '555-123-4567',
  other_information: 'Test school information'
};

export const schoolsData: SchoolModel[] = [
  {
    id: 1,
    school_name: 'Test Elementary School',
    address_line_1: '123 Main Street',
    address_line_2: 'Suite 100',
    contact_phone: '555-123-4567',
    other_information: 'Test school information'
  },
  {
    id: 2,
    school_name: 'Another Test School',
    address_line_1: '456 Oak Avenue',
    address_line_2: '',
    contact_phone: '555-987-6543',
    other_information: 'Another test school'
  }
];

export const schoolCreateAndEditData: SchoolCreateAndEditModel = {
  school_name: 'Updated Test School',
  address_line_1: '789 Updated Street',
  address_line_2: 'Floor 2',
  contact_phone: '555-111-2222',
  other_information: 'Updated school information'
};

export const deletionResponseSuccess: DeletionResponse = {
  id: 1,
  message: 'School deleted successfully'
};

export const httpSchoolCreateError1 = {
  school_name: ['This field is required.'],
  contact_phone: ['Enter a valid phone number.']
};

export const httpSchoolEditError1 = {
  address_line_1: ['This field is required.'],
  contact_phone: ['Enter a valid phone number.']
};

export const httpSchoolDeleteError1 = {
  detail: 'You do not have permission to perform this action.'
};
