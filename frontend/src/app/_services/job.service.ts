import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { AccountService } from './account.service';
import { environment } from '@environments/environment';


const baseUrl = `${environment.apiUrl}/jobs`;

@Injectable({ providedIn: 'root' })
export class JobService {

  constructor(private http: HttpClient, private accountService: AccountService) { }

  getAllJobs() {
    const account = this.accountService.accountValue;
    return this.http.post<any[]>(`${baseUrl}/get`, { 'api_keys': account?.apiKeys });
  }

  getJobById(uuid: string) {
    const account = this.accountService.accountValue;
    return this.http.post<any>(`${baseUrl}/get/${uuid}`, { 'api_keys': account?.apiKeys });
  }

  getJobResults(uuid: string) {
    const account = this.accountService.accountValue;
    return this.http.post<any>(`${baseUrl}/results/${uuid}`, { 'api_keys': account?.apiKeys });
  }

  createJob(job: any) {
    const account = this.accountService.accountValue;
    return this.http.post<any>(`${baseUrl}/create`, { 'job': job, 'api_keys': account?.apiKeys });
  }

  deleteJob(uuid: string) {
    const account = this.accountService.accountValue;
    return this.http.post<any>(`${baseUrl}/delete/${uuid}`, { 'api_keys': account?.apiKeys });
  }
}
