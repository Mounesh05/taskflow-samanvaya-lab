
import { describe, expect, it } from "vitest";

import type { Task } from "./api";

import {
  sortByPriority,
  linearTaskSearch,
  countByStatus,
} from "./algorithms";

const tasks: Task[] = [
  {
    id: "1",
    title: "Create API",
    priority: 5,
    status: "todo",
  },
  {
    id: "2",
    title: "Fix dashboard",
    priority: 2,
    status: "in_progress",
  },
  {
    id: "3",
    title: "Test API",
    priority: 3,
    status: "done",
  },
];

describe("Task algorithms", () => {
  it("sorts tasks by descending priority", () => {
    const result = sortByPriority(tasks);
    expect(result.map((task) => task.priority))
      .toEqual([5, 3, 2]);
  });

  it("does not mutate the input", () => {
    const original = [...tasks];

    sortByPriority(tasks);

    expect(tasks).toEqual(original);
  });

  it("searches without case sensitivity", () => {
    const result = linearTaskSearch(tasks, "api");
    expect(result).toHaveLength(2);
  });

  it("counts task statuses", () => {
    expect(countByStatus(tasks)).toEqual({
      todo: 1,
      in_progress: 1,
      done: 1,
    });
  });

  it("handles empty collections", () => {
    expect(countByStatus([])).toEqual({
      todo: 0,
      in_progress: 0,
      done: 0,
    });
  });
});
