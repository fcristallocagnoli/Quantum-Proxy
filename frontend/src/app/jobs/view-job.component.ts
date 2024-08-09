import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AlertService } from '@app/_services';
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
        private alertService: AlertService
    ) { }

    basicData: any;
    dataSimplified: boolean = false;

    basicOptions: any;
    darkThemeOptions: any;
    lightThemeOptions: any;

    ngOnInit(): void {
        this.setThemeOptions();
        const uuid = this.route.snapshot.params['uuid']
        this.jobService.getJobById(uuid)
            .pipe(first())
            .subscribe(job => {
                this.job = job;
                this.jobService.getJobResults(uuid)
                    .pipe(first())
                    .subscribe(results => {
                        this.results = results;
                        this.buildData();
                    });
            });
    }

    copyToClipboard(text: any) {
        navigator.clipboard.writeText(text).then(() => {
            this.alertService.info('Job UUID copied to clipboard');
        }, (err) => {
            this.alertService.error('Could not copy text: ', err);
        });
    }

    private setThemeOptions() {
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color');
        const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
        const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

        this.darkThemeOptions = {
            plugins: {
                legend: {
                    labels: {
                        color: textColor
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        color: textColorSecondary
                    },
                    grid: {
                        color: surfaceBorder,
                        drawBorder: false
                    }
                },
                x: {
                    ticks: {
                        color: textColorSecondary
                    },
                    grid: {
                        color: surfaceBorder,
                        drawBorder: false
                    }
                }
            }
        };
        this.lightThemeOptions = {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                },
            }
        };
        this.basicOptions = this.getPreferredTheme() === 'dark' ?
            this.darkThemeOptions : this.lightThemeOptions;
    }

    private getPreferredTheme(): string {
        const storedTheme = localStorage.getItem('theme');
        if (storedTheme) {
            return storedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    private buildData(simplified: boolean = false) {
        const results = this.results;
        let labels = Object.keys(results);
        let data = Object.values(results).map(value => Number(value));

        if (!simplified) {
            let maxLabel = Math.max(...labels.map(key => Number(key)));
            let newDict: { [key: string]: any } = {};
            for (let i = 0; i <= maxLabel; i++) {
                newDict[i.toString(2)] = results[i] ?? 0;
            }

            labels = Object.keys(newDict);
            data = Object.values(newDict);
            labels = labels.map(label => label.padStart(this.job.qubits, '0'));
        }

        labels = labels.map(label => "State " + label);

        this.basicData = {
            labels: labels,
            datasets: [
                {
                    label: 'Probabillity',
                    data: data,
                    backgroundColor: ['rgba(0, 95, 143, 0.6)'],
                    borderColor: ['rgb(0, 95, 143)'],
                    borderWidth: 1
                }
            ]
        };
    }

    simplifyResults() {
        this.dataSimplified = !this.dataSimplified;
        this.buildData(this.dataSimplified);
    }
}
