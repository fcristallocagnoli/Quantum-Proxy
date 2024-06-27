import { Component, OnInit } from '@angular/core';
import { AlertService } from '@app/_services';
import { JobService } from '@app/_services/job.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { CreateJobComponent } from './create-job.component';
import { first } from 'rxjs';

@Component({
    templateUrl: './jobs.component.html',
})
export class JobsComponent implements OnInit {
    account?: any;
    jobs?: any[];

    isDeleting: boolean = false;
    deletingId?: string;

    isRefreshingJobs: boolean = false;

    constructor(
        private jobService: JobService,
        private alertService: AlertService,
        private modalService: NgbModal,
    ) { }

    ngOnInit(): void {
        this.jobService.getAllJobs()
            .subscribe(jobs => {
                this.jobs = jobs;
            });
    }

    copyToClipboard(text: any) {
        navigator.clipboard.writeText(text).then(() => {
            this.alertService.info('Job UUID copied to clipboard');
        }, (err) => {
            this.alertService.error('Could not copy text: ', err);
        });
    }

    getShortUUID(uuid: string) {
        return uuid.substring(0, 8);
    }

    timeSince(date: number) {
        const now = new Date();
        const pastDate = new Date(date);
        const secondsPast = Math.floor((now.getTime() - pastDate.getTime()) / 1000);

        const oneMinute = 60;
        const oneHour = 60 * 60;
        const oneDay = oneHour * 24;

        if (secondsPast < oneMinute) {
            return `${secondsPast} seconds ago`;
        }
        if (secondsPast < oneHour) {
            const minutes = Math.floor(secondsPast / oneMinute);
            return `${minutes} minutes ago`;
        }
        if (secondsPast < oneDay) {
            const hours = Math.floor(secondsPast / oneHour);
            return `${hours} hours ago`;
        }
        const days = Math.floor(secondsPast / oneDay);
        return `${days} days ago`;
    }

    createJob() {
        let ref = this.modalService.open(CreateJobComponent, { centered: true });
        ref.result.then((resultado) => {
            this.jobService.createJob(resultado).subscribe(() => {
                setTimeout(() => {
                    this.ngOnInit();
                }, 1000);
            });
            this.alertService.info(`Job '${resultado["name"]}' created`);
        }, () => { console.log("Edición cancelada") });
    }

    deleteJob(id: string) {
        this.isDeleting = true;
        this.deletingId = id;
        this.jobService.deleteJob(id)
            .pipe(first())
            .subscribe(() => {
                this.jobs = this.jobs!.filter(x => x.id !== id)
            });
    }

    refreshJobs() {
        this.isRefreshingJobs = true;
        this.jobService.getAllJobs()
            .subscribe(jobs => {
                if (this.jobs?.length !== jobs.length) {
                    this.alertService.success('Jobs updated');
                } else {
                    this.alertService.info('No new jobs');
                }
                this.jobs = jobs;
                this.isRefreshingJobs = false;
            });
    }

}
