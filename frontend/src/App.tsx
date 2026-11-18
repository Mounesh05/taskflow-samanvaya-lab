
import { useEffect, useState } from "react";
import type { FormEvent } from "react";

import {
  getTasks,
  createTask,
  updateTaskStatus,
} from "./api";

import type { Task, TaskStatus } from "./api";

import {
  sortByPriority,
  countByStatus,
  linearTaskSearch,
} from "./algorithms";

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState(3);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function loadTasks() {
    try {
      const result = await getTasks();
      setTasks(result);
      setError("");
    } catch {
      setError("Unable to connect to the TaskFlow backend.");
    }
  }

  useEffect(() => {
    void loadTasks();
  }, []);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (title.trim().length < 3) return;

    setBusy(true);

    try {
      await createTask(title.trim(), priority);
      setTitle("");
      await loadTasks();
    } catch {
      setError("Unable to create the task.");
    } finally {
      setBusy(false);
    }
  }

  async function changeStatus(
    taskId: string,
    status: TaskStatus
  ) {
    try {
      await updateTaskStatus(taskId, status);
      await loadTasks();
    } catch {
      setError("Unable to update task status.");
    }
  }

  const filtered = linearTaskSearch(tasks, search);
  const sorted = sortByPriority(filtered);
  const counts = countByStatus(tasks);

  return (
    <main className="container">
      <header>
        <h1>TaskFlow Lab</h1>
        <p>
          Collaborative test project for SAMANVAYA
        </p>
      </header>

      <section className="summary">
        <article>Total: {tasks.length}</article>
        <article>To do: {counts.todo}</article>
        <article>In progress: {counts.in_progress}</article>
        <article>Done: {counts.done}</article>
      </section>

      <section>
        <h2>Create task</h2>

        <form onSubmit={handleCreate}>
          <input
            value={title}
            onChange={(event) =>
              setTitle(event.target.value)
            }
            minLength={3}
            maxLength={120}
            placeholder="Task title"
            required
          />

          <select
            value={priority}
            onChange={(event) =>
              setPriority(Number(event.target.value))
            }
          >
            {[1, 2, 3, 4, 5].map((value) => (
              <option key={value} value={value}>
                Priority {value}
              </option>
            ))}
          </select>

          <button disabled={busy} type="submit">
            {busy ? "Saving..." : "Add task"}
          </button>
        </form>
      </section>

      <section>
        <h2>Task board</h2>

        <input
          value={search}
          onChange={(event) =>
            setSearch(event.target.value)
          }
          placeholder="Search tasks"
          aria-label="Search tasks"
        />

        {error && <p role="alert">{error}</p>}

        <div className="task-list">
          {sorted.map((task) => (
            <article key={task.id} className="task">
              <div>
                <strong>{task.title}</strong>
                <p>Priority: {task.priority}</p>
              </div>

              <select
                aria-label={`Status for ${task.title}`}
                value={task.status}
                onChange={(event) =>
                  void changeStatus(
                    task.id,
                    event.target.value as TaskStatus
                  )
                }
              >
                <option value="todo">To do</option>
                <option value="in_progress">
                  In progress
                </option>
                <option value="done">Done</option>
              </select>
            </article>
          ))}

          {sorted.length === 0 && (
            <p>No matching tasks.</p>
          )}
        </div>
      </section>
    </main>
  );
}
