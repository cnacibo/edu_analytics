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
};
