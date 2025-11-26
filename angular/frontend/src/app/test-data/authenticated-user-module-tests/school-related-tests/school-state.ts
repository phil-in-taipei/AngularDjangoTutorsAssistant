import { SchoolsState } from 'src/app/authenticated-user/schools/state/school.reducers';
import { SchoolModel } from 'src/app/models/school.model';
import { 
  newlyCreatedSchoolData, 
  schoolData, schoolsData 
} from './school-data';
import { deletionResponseSuccess } from './school-data';
/**
 * Mock NgRx entity-based state data for Schools feature.
 * Pattern follows previously defined mock state structure (ids/entities/message fields).
 */

export const statePriorToSchoolsLoadRequest: SchoolsState = {
  ids: [],
  entities: {},
  deletionModeActivated: false,
  fetchingSchoolsInProgress: false,
  errorMessage: undefined,
  schoolsLoaded: false,
  successMessage: undefined,
};

export const stateAfterSchoolsRequested: SchoolsState = {
  ...statePriorToSchoolsLoadRequest,
  fetchingSchoolsInProgress: true,
};

export const stateAfterSchoolsLoadedSuccess: SchoolsState = {
  ids: schoolsData.map((s) => s.id), // number[]
  entities: {
    [schoolsData[0].id]: schoolsData[0],
    [schoolsData[1].id]: schoolsData[1],
  },
  deletionModeActivated: false,
  fetchingSchoolsInProgress: false,
  errorMessage: undefined,
  schoolsLoaded: true,
  successMessage: undefined,
};

export const stateAfterSchoolsLoadFailure: SchoolsState = {
  ...statePriorToSchoolsLoadRequest,
  errorMessage: 'Error fetching schools!',
};

export const stateAfterSchoolCreatedAdded: SchoolsState = {
  ids: [...(stateAfterSchoolsLoadedSuccess.ids as number[]), newlyCreatedSchoolData.id] as number[],
  entities: {
    ...stateAfterSchoolsLoadedSuccess.entities,
    [newlyCreatedSchoolData.id]: newlyCreatedSchoolData,
  },
  deletionModeActivated: false,
  fetchingSchoolsInProgress: false,
  errorMessage: undefined,
  schoolsLoaded: true,
  successMessage: 'New school successfully submitted!',
};

export const stateAfterSchoolCreationCancelled: SchoolsState = {
  ...stateAfterSchoolsLoadedSuccess,
  errorMessage: 'Error submitting new school!',
  successMessage: undefined,
};

export const stateAfterSchoolEditUpdated: SchoolsState = {
  ids: stateAfterSchoolsLoadedSuccess.ids,
  entities: {
    ...stateAfterSchoolsLoadedSuccess.entities,
    [schoolData.id]: {
      ...stateAfterSchoolsLoadedSuccess.entities[schoolData.id],
      school_name: 'Test School A updated!',
      address_line_1: '789 Updated Street',
      address_line_2: 'Floor 2',
      contact_phone: '555-111-2222',
      other_information: 'Updated school information',
    },
  },
  deletionModeActivated: false,
  fetchingSchoolsInProgress: false,
  errorMessage: undefined,
  schoolsLoaded: true,
  successMessage: 'School information edited!',
};

export const stateAfterSchoolEditCancelled: SchoolsState = {
  ...stateAfterSchoolsLoadedSuccess,
  errorMessage: 'Error! Editing School Failed!',
  successMessage: undefined,
};

export const stateAfterSchoolDeletionModeActivated: SchoolsState = {
  ...stateAfterSchoolsLoadedSuccess,
  deletionModeActivated: true,
};

export const stateAfterSchoolDeletionModeDeactivated: SchoolsState = {
  ...stateAfterSchoolsLoadedSuccess,
  deletionModeActivated: false,
};

export const stateAfterSchoolDeletionSaved: SchoolsState = {
  ids: (stateAfterSchoolsLoadedSuccess.ids as number[]).filter(
    (id: number) => id !== deletionResponseSuccess.id
  ),
  entities: Object.keys(stateAfterSchoolsLoadedSuccess.entities)
    .filter((id) => Number(id) !== deletionResponseSuccess.id)
    .reduce((acc, id) => {
      acc[Number(id)] = stateAfterSchoolsLoadedSuccess.entities[Number(id)]!;
      return acc;
    }, {} as { [id: number]: SchoolModel }),
  deletionModeActivated: false,
  fetchingSchoolsInProgress: false,
  errorMessage: undefined,
  schoolsLoaded: true,
  successMessage: deletionResponseSuccess.message,
};

export const stateAfterSchoolDeletionCancelled: SchoolsState = {
  ...stateAfterSchoolsLoadedSuccess,
  errorMessage: 'Error! School Deletion Failed!',
  successMessage: undefined,
};

export const stateAfterSchoolsMessagesCleared: SchoolsState = {
  ...stateAfterSchoolsLoadedSuccess,
  errorMessage: undefined,
  successMessage: undefined,
};

export const stateAfterSchoolsCleared: SchoolsState = {
  ids: [],
  entities: {},
  deletionModeActivated: false,
  fetchingSchoolsInProgress: false,
  errorMessage: undefined,
  schoolsLoaded: false,
  successMessage: undefined,
};
