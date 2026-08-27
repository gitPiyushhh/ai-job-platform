const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function apiFetch<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export async function getJobs() {
  return apiFetch<any[]>("/api/jobs", {
    cache: "no-store",
  });
}

export async function getApplications() {
  return apiFetch<any[]>("/api/jobs/applications", {
    cache: "no-store",
  });
}

export async function runPipeline() {
  return apiFetch<any>("/api/jobs/pipeline/run", {
    method: "POST",
  });
}