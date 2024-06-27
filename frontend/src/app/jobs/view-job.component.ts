import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { JobService } from '@app/_services/job.service';
import { first } from 'rxjs';

@Component({
    templateUrl: './view-job.component.html',
})
export class ViewJobComponent implements OnInit {
    job: any;

    constructor(
        private route: ActivatedRoute,
        private jobService: JobService,
    ) { }

    ngOnInit(): void {
        const uuid = this.route.snapshot.params['uuid']
        this.jobService.getJobById(uuid)
            .pipe(first())
            .subscribe(job => {
                this.job = job;
            });
    }
}
