import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { JobService } from '@app/_services/job.service';
import { first } from 'rxjs';

@Component({
    templateUrl: './view-job.component.html',
})
export class ViewJobComponent implements OnInit {
    job: any;
    results: any;

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
                this.jobService.getJobResults(uuid)
                    .pipe(first())
                    .subscribe(results => {
                        this.results = results;
                        this.drawHistogram();
                    });
            });
    }

    private drawHistogram() {
        const results = this.results;
        let labels = Object.keys(results);
        let data = Object.values(results).map(value => Number(value));

        let maxLabel = Math.max(...labels.map(key => Number(key)));
        let newDict: { [key: string]: any } = {};
        for (let i = 0; i <= maxLabel; i++) {
            newDict[i.toString(2)] = results[i] ?? 0;
        }

        labels = Object.keys(newDict);
        data = Object.values(newDict);

        const canvas: any = document.getElementById('histogram');
        const ctx = canvas.getContext('2d');

        const chartWidth = canvas.width;
        const chartHeight = canvas.height;
        const barWidth = chartWidth / labels.length;
        // const barWidth = chartWidth / (labels.length * 2);

        const maxValue = 1.0;

        ctx.clearRect(0, 0, chartWidth, chartHeight);
        ctx.fillStyle = '#007bff';

        data.forEach((value, index) => {
            const barHeight = (value / maxValue) * chartHeight;
            const x = index * barWidth;
            const y = chartHeight - barHeight;
            ctx.fillRect(x, y, barWidth, barHeight);
        });
        
        ctx.fillStyle = '#000';
        ctx.textAlign = 'center';
        
        labels.forEach((label, index) => {
            const x = index * barWidth + barWidth / 2;
            const y = chartHeight - 5;
            ctx.fillText(label.padStart(this.job.qubits, '0'), x, y);
        });
    }
}
