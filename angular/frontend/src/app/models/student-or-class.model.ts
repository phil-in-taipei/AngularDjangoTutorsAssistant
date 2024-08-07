
export interface StudentOrClassModel {
    id: number;
    student_or_class_name: string;
    account_type: string;
    school: number | undefined;
    comments: string;
    purchased_class_hours: number | undefined;
    tuition_per_hour: number;
    account_id: string;
    slug: string;
}
