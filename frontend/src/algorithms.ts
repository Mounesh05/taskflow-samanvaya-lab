
import type { Task } from "./api";

export function sortByPriority(tasks: Task[]): Task[] {
  return [...tasks].sort(
    (a, b) => b.priority - a.priority
  );
}

export function linearTaskSearch(
  tasks: Task[],
  keyword: string
): Task[] {
  const query = keyword.toLowerCase();

  return tasks.filter((task) =>
    task.title.toLowerCase().includes(query)
  );
}

export function countByStatus(
  tasks: Task[]
): Record<Task["status"], number> {
  return tasks.reduce(
    (counts, task) => {
      counts[task.status] += 1;
      return counts;
    },
    {
      todo: 0,
      in_progress: 0,
      done: 0,
    }
  );
}
