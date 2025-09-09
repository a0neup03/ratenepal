// TypeScript types for the Nepal Office Tracker

export interface District {
  name: string;
  province: string;
}

export interface Province {
  name: string;
  districts: string[];
}

export interface OfficeType {
  office_type: string;
  display_name: string;
  display_name_nepali: string;
  count: number;
}

export interface Office {
  id: number;
  office_id: string;
  name: string;
  name_nepali: string;
  address?: string;
  phone?: string;
  website?: string;
}

export interface Service {
  service_id: string;
  service_name: string;
  service_name_nepali: string;
  estimated_time?: string;
  fees?: any;
}

export interface Visit {
  visit_id: number;
  start_time: string;
  office_name: string;
  service_name: string;
}

export enum ServiceStatus {
  SUCCESS = "kaam_bhayo",
  FAILED = "kaam_bhayena",
  IN_PROGRESS = "chalirahe"
}

export interface Rating {
  visit_id: number;
  overall_rating: number;
  staff_behavior_rating: number;
  office_cleanliness_rating: number;
  process_efficiency_rating: number;
  information_clarity_rating: number;
  asked_for_bribe?: boolean;
  staff_helpful?: boolean;
  process_clear?: boolean;
  documents_sufficient?: boolean;
  would_recommend?: boolean;
  wait_reason?: string;
  suggestions?: string;
  complaints?: string;
}

export interface OfficeAnalytics {
  office_id: number;
  office_name: string;
  office_name_nepali?: string;
  district: string;
  province: string;
  total_visits: number;
  successful_visits: number;
  failed_visits: number;
  success_rate: number;
  avg_overall_rating: number;
  avg_staff_behavior: number;
  avg_cleanliness: number;
  avg_efficiency: number;
  avg_information_clarity: number;
  avg_wait_time_minutes: number;
  bribe_reports: number;
  bribe_rate: number;
}

export interface FeedbackQuestion {
  id: string;
  question_nepali: string;
  question_english: string;
  type: 'boolean' | 'text' | 'number';
  critical: boolean;
}