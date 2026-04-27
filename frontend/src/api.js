const API_BASE_URL = process.env.REACT_APP_API_URL;

class ApiService {
  constructor() {
    this.base_url = API_BASE_URL;
  }

  async get_programs(source, params = {}) {
    const url = new URL(`${this.base_url}/${source}`);
    Object.keys(params).forEach((key) => url.searchParams.append(key, params[key]));
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async get_program(source, program_id) {
    const url = new URL(`${this.base_url}/${source}/${program_id}`);
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async get_courses(program_id, params, source = 'hse') {
    const url = new URL(`${this.base_url}/${source}/${program_id}/courses`);
    Object.keys(params).forEach((key) => url.searchParams.append(key, params[key]));
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async get_vuz_programs_stats(stat_name) {
    let url;
    switch (stat_name) {
      case 'total_programs':
        url = new URL(`${this.base_url}/stats/metrics/vuz_programs_count`);
        break;
      case 'avg_cost':
        url = new URL(`${this.base_url}/stats/metrics/vuz_programs_avg_cost`);
        break;
      case 'min_score':
        url = new URL(`${this.base_url}/stats/metrics/vuz_programs_min_paid_score`);
        break;
      case 'max_score':
        url = new URL(`${this.base_url}/stats/metrics/vuz_programs_max_budget_score`);
        break;
      default:
    }
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async get_sphere_data() {
    const url = new URL(`${this.base_url}/stats/spheres/vuz_spheres_distribution`);
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async get_top_programs_vuz_by_cost() {
    const url = new URL(`${this.base_url}/stats/cost/top_programs_vuz_by_cost`);
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }

  async get_avg_cost_top10() {
    const url = new URL(`${this.base_url}/stats/cost/vuz_avg_cost_top10`);
    const response = await fetch(url, {
      method: 'GET',
      mode: 'cors',
      credentials: 'omit',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  }
}

const api = new ApiService();

export const hseApi = {
  getPrograms: (params) => api.get_programs('hse', params),
  getProgram: (program_id) => api.get_program('hse', program_id),
  getCourses: (program_id, params) => api.get_courses(program_id, params),
};

export const vuzopediaApi = {
  getPrograms: (params) => api.get_programs('vuzopedia', params),
  getProgram: (program_id) => api.get_program('vuzopedia', program_id),
  getTotalPrograms: () => api.get_vuz_programs_stats('total_programs'),
  getAvgCost: () => api.get_vuz_programs_stats('avg_cost'),
  getMinScore: () => api.get_vuz_programs_stats('min_score'),
  getMaxScore: () => api.get_vuz_programs_stats('max_score'),
  getSphereData: () => api.get_sphere_data(),
  getTopProgramsByCost: () => api.get_top_programs_vuz_by_cost(),
  getAvgCostTopTen: () => api.get_avg_cost_top10(),
};
