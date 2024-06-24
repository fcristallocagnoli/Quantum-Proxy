export interface System {
    id: string;
    provider: { provider_id: string, provider_name: string, provider_from?: string };
    bid: string;
    backend_name: string;
    
    // -- extra fields (in common) --
    status?: string;
    qubits?: number;
    queue?: { type: string, value: string };

    // -- extra fields (ionq) --
    degraded?: boolean;
    has_access?: boolean;
    characterization?: { [key: string]: any };

    // -- extra fields (braket) --
    gates_supported?: string[];
    shots_range?: { min: number, max: number };
    device_cost?: { price: number, unit: string };

    // -- extra fields (rigetti) --
    rep_rate?: string;
    median_t1?: string;
    median_t2?: string;
    median_sim_1q_fidelity?: string;
    median_2q_xy_fidelity?: string;
    median_2q_cz_fidelity?: string;
    median_ro_fidelity?: string;
    median_Active_reset_fidelity?: string;

    // -- extra fields (ibm) --
    basis_gates?: string[];
    clops_h?: number;
    credits_required?: boolean;
    max_experiments?: number;
    max_shots?: number;

    extra: string[];
    last_checked: string;
}