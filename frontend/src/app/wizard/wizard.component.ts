import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Provider, System } from '@app/_models';
import { ProviderService, SystemService } from '@app/_services';
import { first } from 'rxjs';

@Component({
  templateUrl: './wizard.component.html',
})
export class WizardComponent implements OnInit {
  systems: System[];
  subSystems: System[];

  sort: string = 'Qubits';
  statusFilter: string = 'All';

  currentPage = 1;
  pageSize = 3;

  form: FormGroup;

  responsiveOptions: any[] = [
    {
        breakpoint: '1199px',
        numVisible: 2,
        numScroll: 1
    },
    {
        breakpoint: '991px',
        numVisible: 1,
        numScroll: 1
    },
  ];

  constructor(
    private providerService: ProviderService,
    private systemService: SystemService,
    private formBuilder: FormBuilder,
  ) { }

  dataStructure: { provider: any, systems: any }[] = [];
  dataStructureFiltered: { provider: any, systems: any }[] = [];

  ngOnInit() {
    this.getData();
    this.form = this.formBuilder.group({
      qubits: ['', [Validators.min(0), Validators.max(1000)]],
      supportedGates: [''],
      queueTime: ['', Validators.pattern(/^(\d+d)$|^(\d+hrs)$|^(\d+min)$/)],
      queuedJobs: ['', Validators.min(0)],
      pricePerTask: ['', Validators.min(0)],
      pricePerShot: ['', Validators.min(0)],
    });
  }

  getData() {
    let dataStructure: any[] = [];
    this.systemService.getAll()
      .pipe(first())
      .subscribe(systems => {
        this.systems = systems;
        this.updateSystems(this.currentPage);

        this.providerService.getAll()
          .pipe(first())
          .subscribe(providers => {
            providers.forEach(provider => {
              let minimalProvider = {
                name: provider.name,
                pid: provider.pid,
                description: provider.description,
                website: provider.website,
                thirdParty: provider.third_party?.third_party_name,
                lastChecked: provider.last_checked
              }
              let providerSystems = this.systems.filter(system => {
                return system.provider.provider_id === provider["id"];
              });
              dataStructure.push({ provider: minimalProvider, systems: providerSystems });
            });
            // filter out providers with no systems
            this.dataStructure = dataStructure.filter(elem => elem["systems"].length > 0);
            this.filterSystems();
          });
      });
  }

  updateSystems(currentPage: number) {
    this.subSystems = this.systems.slice(
      (currentPage - 1) * this.pageSize, currentPage * this.pageSize
    );
  }

  setSort(sort: string) {
    this.sort = sort;
  }

  filterSystemsForm() {
    let qubits = this.form.controls['qubits'].value;
    let supportedGates: string = this.form.controls['supportedGates'].value;
    let queueTime = this.form.controls['queueTime'].value;
    let queuedJobs = this.form.controls['queuedJobs'].value;
    let pricePerTask = this.form.controls['pricePerTask'].value;
    let pricePerShot = this.form.controls['pricePerShot'].value;

    this.dataStructureFiltered = this.dataStructure.map(provider => {
      return {
        provider: provider.provider,
        systems: provider.systems.filter((system: System) => {
          let passes = true;
          if (qubits !== '' && (system.qubits ?? Infinity) < qubits) {
            passes = false;
          }
          if (supportedGates !== '') {
            const gates_supported = system.gates_supported ?? [];
            const basis_gates = system.basis_gates ?? [];
            let gateField1 = supportedGates.split(',').every(gate => gates_supported.includes(gate));
            let gateField2 = supportedGates.split(',').every(gate => basis_gates.includes(gate));
            passes = passes && (gateField1 || gateField2);
          }
          if (queueTime !== '') {
            if (system.queue && system.queue?.type === "avg_time") {
              passes = passes && this.toMilliseconds(system.queue.value) <= this.toMilliseconds(queueTime);
            } else {
              passes = false;
            }
          }
          if (queuedJobs !== '') {
            if (system.queue && system.queue?.type === "jobs_remaining") {
              passes = passes && parseInt(system.queue.value) <= queuedJobs;
            } else {
              passes = false;
            }
          }
          if (pricePerTask !== '' && system.price?.per_task_price !== undefined) {
            passes = passes && system.price.per_task_price <= parseFloat(pricePerTask);
          }
          if (pricePerShot !== '' && system.price?.per_shot_price !== undefined) {
            passes = passes && system.price.per_shot_price <= parseFloat(pricePerShot);
          }
          return passes;
        })
      }
    });
    this.dataStructureFiltered = this.dataStructureFiltered.filter(elem => elem["systems"].length > 0);
    this.sortSystems(this.sort);
  }

  filterSystems(statusFilter: string = 'All') {
    let online = ["online", "running", "available"];
    let offline = ["offline", "calibrating", "reserved"];
    this.statusFilter = statusFilter;
    switch (statusFilter) {
      case 'All':
        this.dataStructureFiltered = this.dataStructure;
        break;
      case 'Online':
        this.dataStructureFiltered = this.dataStructure.map(provider => {
          return {
            provider: provider.provider,
            systems: provider.systems.filter(
              (system: System) => online.includes(system.status?.toLowerCase() ?? 'N/A')
            )
          }
        });
        this.dataStructureFiltered = this.dataStructureFiltered.filter(elem => elem["systems"].length > 0);
        break;
      case 'Offline':
        this.dataStructureFiltered = this.dataStructure.map(provider => {
          return {
            provider: provider.provider,
            systems: provider.systems.filter(
              (system: System) => offline.includes(system.status?.toLowerCase() ?? 'N/A')
            )
          }
        });
        this.dataStructureFiltered = this.dataStructureFiltered.filter(elem => elem["systems"].length > 0);
        break;
    }
    this.sortSystems(this.sort);
  }

  sortSystems(sort: string = 'Qubits') {
    this.sort = sort;
    switch (sort) {
      case 'Qubits':
        this.dataStructureFiltered = this.dataStructureFiltered.map(provider => {
          // ordenamos los sistemas de cada proveedor
          return {
            provider: provider.provider,
            systems: provider.systems.sort((a: System, b: System) => b.qubits! - a.qubits!)
          }
          // y luego ordenamos los proveedores
        }).sort((a, b) => b.systems[0].qubits! - a.systems[0].qubits!);
        break;
      case 'Queue':
        this.dataStructureFiltered = this.dataStructureFiltered.map(provider => {
          // ordenamos los sistemas de cada proveedor
          return {
            provider: provider.provider,
            systems: provider.systems.sort((a: System, b: System) => {
              return this.sortByQueue(a.queue, b.queue);
            })
          }
          // y luego ordenamos los proveedores
        }).sort((a, b) => {
          return this.sortByQueue(a.systems[0].queue, b.systems[0].queue);
        });
        break;
      case 'Price':
        this.dataStructureFiltered = this.dataStructureFiltered.map(provider => {
          // ordenamos los sistemas de cada proveedor
          return {
            provider: provider.provider,
            systems: provider.systems.sort((a: System, b: System) => {
              return this.sortByPrice(a.price, b.price);
            })
          }
          // y luego ordenamos los proveedores
        }).sort((a, b) => {
          return this.sortByPrice(a.systems[0].price, b.systems[0].price);
        });
        break;
    }
  }

  onSubmit() {
    this.filterSystemsForm();
  }

  countSystems() {
    let count = 0;
    this.dataStructureFiltered.forEach(provider => {
      count += provider.systems.length;
    });
    return count;
  }

  // transforms strings like '5d 10hrs 15min' to milliseconds
  private toMilliseconds(formato: string): number {
    const diasRegex = /(\d+)d/;
    const horasRegex = /(\d+)hrs/;
    const minsRegex = /(\d+)min/;

    let dias = 0, horas = 0, mins = 0;

    const diasMatch = formato.match(diasRegex);
    if (diasMatch) {
      dias = parseInt(diasMatch[1]);
    }

    const horasMatch = formato.match(horasRegex);
    if (horasMatch) {
      horas = parseInt(horasMatch[1]);
    }

    const minsMatch = formato.match(minsRegex);
    if (minsMatch) {
      mins = parseInt(minsMatch[1]);
    }

    return ((dias * 24 * 60) + (horas * 60) + mins) * 60 * 1000;
  }

  private sortByQueue(aQueue: any, bQueue: any): number {
    if (aQueue === undefined && bQueue === undefined)
      return 0;
    else if (aQueue === undefined)
      return 1;
    else if (bQueue === undefined)
      return -1;

    let comparison = 0;
    if (aQueue.type === 'avg_time' && bQueue.type === 'avg_time') {
      comparison = this.toMilliseconds(aQueue.value) - this.toMilliseconds(bQueue.value);
    } else if (aQueue.type === 'jobs_remaining' && bQueue.type === 'jobs_remaining') {
      comparison = parseInt(aQueue.value) - parseInt(bQueue.value);
    }
    return comparison;
  }

  private sortByPrice(aPrice: any, bPrice: any): number {
    if (aPrice === undefined && bPrice === undefined)
      return 0;
    else if (aPrice === undefined)
      return 1;
    else if (bPrice === undefined)
      return -1;

    let comparison = 0;
    if (aPrice.per_shot_price !== undefined && bPrice.per_shot_price !== undefined) {
      comparison = aPrice.per_shot_price - bPrice.per_shot_price;
    } else if (aPrice.per_task_price !== undefined && bPrice.per_task_price !== undefined) {
      comparison = aPrice.per_task_price - bPrice.per_task_price;
    } else if (aPrice.per_minute_price !== undefined && bPrice.per_minute_price !== undefined) {
      comparison = aPrice.per_minute_price - bPrice.per_minute_price;
    }
    return comparison;
  }

  // Convierte tiempo en milisegundos a tiempo de espera con el formato de IonQ
  convertFromMs(millisecStr: string | undefined): string {
    if (millisecStr === undefined) {
      return "N/A";
    }
    let millisec = parseInt(millisecStr);

    // Convertir milisegundos a segundos
    let seconds = Math.floor(millisec / 1000);

    // Calcular días, horas y minutos
    const mins = Math.floor(seconds / 60);
    seconds = seconds % 60;
    const hours = Math.floor(mins / 60);
    const minutes = mins % 60;
    const days = Math.floor(hours / 24);
    const remainingHours = hours % 24;

    let avgTimeInQueue = "";

    if (days > 30) {
      avgTimeInQueue = "> 1month";
    } else if (days > 1) {
      avgTimeInQueue = `${days}d ${remainingHours}hrs ${minutes}min`;
    } else if (remainingHours > 1) {
      avgTimeInQueue = `${remainingHours}hrs ${minutes}min`;
    } else if (minutes > 1) {
      avgTimeInQueue = `${minutes}min`;
    } else {
      avgTimeInQueue = "< 1min";
    }

    return avgTimeInQueue;
  }

}
