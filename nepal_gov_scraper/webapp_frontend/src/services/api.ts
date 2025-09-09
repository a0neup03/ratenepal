// API service functions for Nepal Office Tracker

import axios from 'axios';
import { District, OfficeType, Office, Service, Visit, Rating, ServiceStatus, OfficeAnalytics } from '../types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Office Selection APIs
export const getDistricts = async (): Promise<{ districts: string[], provinces: Record<string, string[]> }> => {
  const response = await api.get('/api/selection/districts');
  return response.data;
};

export const getOfficeTypes = async (district: string): Promise<OfficeType[]> => {
  const response = await api.get(`/api/selection/office-types/${district}`);
  return response.data;
};

export const getOffices = async (district: string, officeType: string): Promise<{ offices: Office[] }> => {
  const response = await api.get(`/api/selection/offices/${district}/${officeType}`);
  return response.data;
};

export const getServices = async (officeId: number): Promise<{ office_name: string, services: Service[] }> => {
  const response = await api.get(`/api/selection/services/${officeId}`);
  return response.data;
};

// Visit Tracking APIs
export const startTimer = async (officeId: number, serviceId: number, userId?: number): Promise<Visit> => {
  const response = await api.post('/api/visit/start-timer', {
    office_id: officeId,
    service_id: serviceId,
    user_id: userId,
  });
  return response.data;
};

export const endVisit = async (visitId: number, serviceStatus: ServiceStatus): Promise<any> => {
  const response = await api.post('/api/visit/end-visit', {
    visit_id: visitId,
    service_status: serviceStatus,
  });
  return response.data;
};

export const submitRating = async (rating: Rating): Promise<any> => {
  const response = await api.post('/api/visit/rating', rating);
  return response.data;
};

export const getVisitStatus = async (visitId: number): Promise<any> => {
  const response = await api.get(`/api/visit/visit-status/${visitId}`);
  return response.data;
};

// Feedback Questions
export const getFeedbackQuestions = async (): Promise<any> => {
  const response = await api.get('/api/visit/feedback-questions');
  return response.data;
};

export const getWaitReasonOptions = async (): Promise<any> => {
  const response = await api.get('/api/visit/wait-reasons');
  return response.data;
};

// Analytics APIs
export const getDashboardData = async (): Promise<any> => {
  const response = await api.get('/api/analytics/dashboard');
  return response.data;
};

export const getOfficeAnalytics = async (officeId: number): Promise<OfficeAnalytics> => {
  const response = await api.get(`/api/analytics/office/${officeId}`);
  return response.data;
};

export const compareOffices = async (officeIds: number[], metrics: string[]): Promise<any> => {
  const response = await api.post('/api/analytics/compare', {
    office_ids: officeIds,
    metrics: metrics,
  });
  return response.data;
};

export const getOfficeRankings = async (
  scope: string,
  province?: string,
  district?: string,
  metric?: string,
  limit?: number
): Promise<any> => {
  const params = new URLSearchParams();
  if (province) params.append('province', province);
  if (district) params.append('district', district);
  if (metric) params.append('metric', metric);
  if (limit) params.append('limit', limit.toString());
  
  const response = await api.get(`/api/analytics/rankings/${scope}?${params.toString()}`);
  return response.data;
};

// Test APIs (for development)
export const getTestDistricts = async (): Promise<any> => {
  const response = await api.get('/test/districts');
  return response.data;
};

export const getTestOfficeTypes = async (): Promise<any> => {
  const response = await api.get('/test/office-types');
  return response.data;
};

export const testTimer = async (): Promise<any> => {
  const response = await api.post('/test/timer');
  return response.data;
};

export const testRating = async (): Promise<any> => {
  const response = await api.post('/test/rating');
  return response.data;
};