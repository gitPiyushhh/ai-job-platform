"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import {
  getApplications,
  getJobs,
  runPipeline,
} from "../../lib/api";

type Job = {
  id: number;
  title: string;
  company: string;
  location?: string;
  match_score?: number;
  recommendation?: string;
  skills?: string;
  best_resume?: string;
  job_url?: string;
  match_reason?: string;
};

export default function Home() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [applications, setApplications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState("");

  async function loadDashboard() {
    try {
      setLoading(true);

      const [jobData, applicationData] = await Promise.all([
        getJobs(),
        getApplications(),
      ]);

      setJobs(jobData);
      setApplications(applicationData);
    } catch (error) {
      console.error(error);
      setMessage(
        "Unable to connect to backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  async function handleRunPipeline() {
    try {
      setRunning(true);
      setMessage("Searching and matching jobs...");

      await runPipeline();

      await loadDashboard();

      setMessage("Job search completed successfully.");
    } catch (error) {
      console.error(error);
      setMessage("Pipeline failed. Check the backend terminal.");
    } finally {
      setRunning(false);
    }
  }

  const applyJobs = jobs.filter(
    (job) => job.recommendation === "APPLY"
  );

  const reviewJobs = jobs.filter(
    (job) => job.recommendation === "REVIEW"
  );

  const topJobs = [...jobs]
    .filter((job) => job.match_score !== null && job.match_score !== undefined)
    .sort(
      (a, b) =>
        (b.match_score || 0) -
        (a.match_score || 0)
    )
    .slice(0, 6);

  return (
    <div className="app">

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">AI</div>

          <div>
            <div className="brand-name">JobPilot</div>
            <div className="brand-subtitle">
              AI Job Assistant
            </div>
          </div>
        </div>

        <nav className="nav">
          <Link
            href="/"
            className="nav-item active"
          >
            Dashboard
          </Link>

          <Link
            href="/jobs"
            className="nav-item"
          >
            Jobs
          </Link>

          <Link
            href="/applications"
            className="nav-item"
          >
            Applications
          </Link>

          <Link
            href="/resumes"
            className="nav-item"
          >
            Resumes
          </Link>
        </nav>

        <div className="automation-box">
          <div className="automation-row">
            <div className="online-dot" />

            <div>
              <div className="automation-title">
                Automation Active
              </div>

              <div className="automation-time">
                8 AM · 8 PM
              </div>
            </div>
          </div>
        </div>
      </aside>

      <main className="main">

        <header className="header">
          <div>
            <h1>
              Good morning, Piyush 👋
            </h1>

            <p>
              Here are your latest AI-matched opportunities.
            </p>
          </div>

          <button
            className="primary-btn"
            onClick={handleRunPipeline}
            disabled={running}
          >
            {running
              ? "Running..."
              : "Run Job Search"}
          </button>
        </header>

        {message && (
          <div
            style={{
              marginBottom: 20,
              padding: 12,
              borderRadius: 9,
              background: "#efefff",
              color: "#5146b8",
              fontSize: 13,
            }}
          >
            {message}
          </div>
        )}

        <section className="stats">

          <div className="stat">
            <div className="stat-label">
              Jobs Found
            </div>

            <div className="stat-value">
              {jobs.length}
            </div>

            <div className="stat-description">
              From latest search
            </div>
          </div>

          <div className="stat">
            <div className="stat-label">
              Apply Recommended
            </div>

            <div className="stat-value">
              {applyJobs.length}
            </div>

            <div className="stat-description">
              Strong matches
            </div>
          </div>

          <div className="stat">
            <div className="stat-label">
              Review
            </div>

            <div className="stat-value">
              {reviewJobs.length}
            </div>

            <div className="stat-description">
              Need your decision
            </div>
          </div>

          <div className="stat">
            <div className="stat-label">
              Applications
            </div>

            <div className="stat-value">
              {applications.length}
            </div>

            <div className="stat-description">
              Being tracked
            </div>
          </div>

        </section>

        <section className="section">

          <div className="section-header">
            <div className="section-title">
              Recommended Jobs
            </div>

            <Link
              href="/jobs"
              className="section-link"
            >
              View all →
            </Link>
          </div>

          {loading ? (
            <div className="loading">
              Loading jobs...
            </div>
          ) : topJobs.length === 0 ? (
            <div className="loading">
              No AI-matched jobs yet. Run a job search.
            </div>
          ) : (
            <div className="jobs">

              {topJobs.map((job) => (

                <article
                  className="job"
                  key={job.id}
                >

                  <div className="job-top">

                    <div>
                      <div className="job-title">
                        {job.title}
                      </div>

                      <div className="job-company">
                        {job.company}
                      </div>
                    </div>

                    <div className="match">
                      {job.match_score}%
                    </div>

                  </div>

                  <div className="job-meta">
                    📍 {job.location || "Location not specified"}
                  </div>

                  {job.skills && (
                    <div className="skills">
                      {job.skills
                        .split(",")
                        .slice(0, 5)
                        .map((skill) => (
                          <span
                            className="skill"
                            key={skill}
                          >
                            {skill.trim()}
                          </span>
                        ))}
                    </div>
                  )}

                  <div className="job-bottom">

                    <div className="resume">
                      Resume:{" "}
                      <strong>
                        {job.best_resume || "—"}
                      </strong>
                    </div>

                    {job.job_url && (
                      <a
                        className="apply"
                        href={job.job_url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        APPLY NOW ↗
                      </a>
                    )}

                  </div>

                </article>

              ))}

            </div>
          )}

        </section>

      </main>
    </div>
  );
}