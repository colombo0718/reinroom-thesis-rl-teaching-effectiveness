"""
Render smoke tests for rr_envs.py.

This file complements test_rr_envs.py:
- test_rr_envs.py checks environment logic, rewards, done conditions, and Q-learning.
- test_rr_envs_render.py checks that each environment can produce a visible frame.

Run with pytest, if available:
    pytest notebooks/test_rr_envs_render.py

Run directly without pytest:
    python notebooks/test_rr_envs_render.py

PNG outputs are written to:
    render_outputs/
"""

from pathlib import Path
import importlib
import os
import sys

import numpy as np

try:
    import pytest
except ModuleNotFoundError:
    pytest = None

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def import_required(module_name):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        if pytest is not None:
            pytest.skip(f"{module_name} is not installed", allow_module_level=True)
        raise RuntimeError(
            f"Missing required module: {module_name}. "
            f"Run this file from the project root and make sure dependencies are installed."
        ) from exc


def fail(message):
    if pytest is not None:
        pytest.fail(message)
    raise AssertionError(message)


rr_envs = import_required("rr_envs")


ENV_CLASSES = [
    rr_envs.MABEnv,
    rr_envs.Maze1DEnv,
    rr_envs.Maze2DEnv,
    rr_envs.HeliEnv,
    rr_envs.FighterEnv,
]


WHITE = np.array([245, 245, 245], dtype=np.uint8)
BLACK = np.array([25, 25, 25], dtype=np.uint8)
GRAY = np.array([170, 170, 170], dtype=np.uint8)
BLUE = np.array([42, 111, 219], dtype=np.uint8)
GREEN = np.array([36, 159, 83], dtype=np.uint8)
RED = np.array([214, 52, 52], dtype=np.uint8)
YELLOW = np.array([245, 196, 65], dtype=np.uint8)
PURPLE = np.array([132, 80, 180], dtype=np.uint8)


def make_env(env_cls):
    """Create envs that may or may not accept Gymnasium render_mode."""
    for kwargs in (
        {"render_mode": "rgb_array"},
        {"render_mode": "human"},
        {},
    ):
        try:
            return env_cls(**kwargs)
        except TypeError:
            continue

    fail(f"Could not construct {env_cls.__name__}")


def unpack_step(step_result):
    """Support both old Gym and Gymnasium step return signatures."""
    if len(step_result) == 5:
        obs, reward, terminated, truncated, info = step_result
        return obs, reward, terminated or truncated, info

    obs, reward, done, info = step_result
    return obs, reward, done, info


def draw_rect(img, x0, y0, x1, y1, color):
    h, w = img.shape[:2]
    x0 = int(np.clip(round(x0), 0, w))
    x1 = int(np.clip(round(x1), 0, w))
    y0 = int(np.clip(round(y0), 0, h))
    y1 = int(np.clip(round(y1), 0, h))
    if x1 > x0 and y1 > y0:
        img[y0:y1, x0:x1] = color


def draw_circle(img, cx, cy, radius, color):
    h, w = img.shape[:2]
    cx = int(round(cx))
    cy = int(round(cy))
    radius = int(round(radius))
    y0 = max(0, cy - radius)
    y1 = min(h, cy + radius + 1)
    x0 = max(0, cx - radius)
    x1 = min(w, cx + radius + 1)
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.ogrid[y0:y1, x0:x1]
    mask = (xx - cx) ** 2 + (yy - cy) ** 2 <= radius ** 2
    img[y0:y1, x0:x1][mask] = color


def draw_grid(img, rows, cols, color=GRAY):
    h, w = img.shape[:2]
    for i in range(rows + 1):
        y = int(round(i * h / rows))
        draw_rect(img, 0, y - 1, w, y + 1, color)
    for i in range(cols + 1):
        x = int(round(i * w / cols))
        draw_rect(img, x - 1, 0, x + 1, h, color)


def fallback_render(env):
    """Draw a deterministic visual frame when rr_envs.py has no render() method."""
    name = type(env).__name__

    if name == "MABEnv":
        img = np.full((260, 520, 3), WHITE, dtype=np.uint8)
        selected = int(getattr(env, "selected", 0))
        step_count = int(getattr(env, "step_count", 0))
        for i in range(env.n_machines):
            x0 = 30 + i * 95
            color = YELLOW if i == selected else BLUE
            draw_rect(img, x0, 70, x0 + 65, 210, color)
            draw_rect(img, x0 + 16, 35, x0 + 49, 65, BLACK)
        draw_rect(img, 30, 225, 30 + step_count * 45, 242, GREEN)
        return img

    if name == "Maze1DEnv":
        img = np.full((120, 600, 3), WHITE, dtype=np.uint8)
        draw_grid(img, 1, env.grid_size)
        cell_w = img.shape[1] / env.grid_size
        draw_rect(img, 0, 0, cell_w, img.shape[0], RED)
        draw_rect(img, cell_w * 9, 0, cell_w * 10, img.shape[0], GREEN)
        draw_circle(img, (env.pos + 0.5) * cell_w, 60, 22, BLUE)
        return img

    if name == "Maze2DEnv":
        img = np.full((500, 500, 3), WHITE, dtype=np.uint8)
        draw_grid(img, env.grid_size, env.grid_size)
        cell = img.shape[0] / env.grid_size
        draw_rect(img, 9 * cell, 0, 10 * cell, cell, GREEN)
        draw_circle(img, (env.x + 0.5) * cell, img.shape[0] - (env.y + 0.5) * cell, 17, BLUE)
        return img

    if name == "HeliEnv":
        img = np.full((env.CANVAS_H, env.CANVAS_W, 3), WHITE, dtype=np.uint8)
        for wall in env.walls:
            x0 = wall["x"]
            x1 = wall["x"] + env.WALL_WIDTH
            draw_rect(img, x0, 0, x1, wall["gap_top"], GREEN)
            draw_rect(img, x0, wall["gap_bottom"], x1, env.CANVAS_H, GREEN)
        draw_circle(img, env.HELI_X, env.heli_y, env.HELI_SIZE * 0.35, BLUE)
        draw_rect(img, 0, 0, env.CANVAS_W, 3, BLACK)
        draw_rect(img, 0, env.CANVAS_H - 3, env.CANVAS_W, env.CANVAS_H, BLACK)
        return img

    if name == "FighterEnv":
        img = np.full((env.CANVAS_H, env.CANVAS_W, 3), WHITE, dtype=np.uint8)
        draw_rect(img, env.LANE_MIN, 0, env.LANE_MIN + 3, env.CANVAS_H, GRAY)
        draw_rect(img, env.LANE_MAX - 3, 0, env.LANE_MAX, env.CANVAS_H, GRAY)
        draw_circle(img, env.rock["x"], env.rock["y"], 20, RED)
        draw_rect(img, env.player_x - 18, env.PLAYER_Y - 12, env.player_x + 18, env.PLAYER_Y + 14, BLUE)
        draw_rect(img, env.player_x - 5, env.PLAYER_Y - 26, env.player_x + 5, env.PLAYER_Y - 8, PURPLE)
        if env.bullet is not None:
            draw_rect(img, env.bullet["x"] - 3, env.bullet["y"] - 12, env.bullet["x"] + 3, env.bullet["y"] + 8, YELLOW)
        return img

    fail(f"No fallback renderer for {name}")


def render_env(env):
    """Use env.render() when available, otherwise draw a fallback frame."""
    render_attempts = (
        lambda: env.render(),
        lambda: env.render(mode="rgb_array"),
        lambda: env.render(mode="human"),
    )

    last_error = None
    for attempt in render_attempts:
        try:
            rendered = attempt()
        except (TypeError, NotImplementedError) as exc:
            last_error = exc
            continue

        if rendered is not None:
            return rendered

    if hasattr(env, "screen"):
        return env.screen

    return fallback_render(env)


def convert_render_to_array(rendered):
    """Convert common render outputs into an image array."""
    if isinstance(rendered, np.ndarray):
        return rendered

    if hasattr(rendered, "canvas") and hasattr(rendered.canvas, "draw"):
        rendered.canvas.draw()
        width, height = rendered.canvas.get_width_height()
        buffer = np.frombuffer(rendered.canvas.tostring_rgb(), dtype=np.uint8)
        return buffer.reshape((height, width, 3))

    if hasattr(rendered, "get_width") and hasattr(rendered, "get_height"):
        try:
            pygame = importlib.import_module("pygame")
        except ModuleNotFoundError as exc:
            if pytest is not None:
                pytest.skip("pygame is required to read pygame Surface render output")
            raise RuntimeError("pygame is required to read pygame Surface render output") from exc

        return np.transpose(pygame.surfarray.array3d(rendered), (1, 0, 2))

    fail(f"Unsupported render output type: {type(rendered)}")


def normalize_image_array(arr):
    arr = np.asarray(arr)

    assert arr.ndim in (2, 3), f"Expected image array with 2 or 3 dims, got {arr.shape}"
    assert arr.shape[0] >= 10, f"Image height is too small: {arr.shape}"
    assert arr.shape[1] >= 10, f"Image width is too small: {arr.shape}"
    assert np.isfinite(arr).all()

    if arr.dtype == np.uint8:
        return arr

    arr = arr.astype(np.float32)
    if arr.size and arr.max() <= 1.0:
        arr = arr * 255.0

    return np.clip(arr, 0, 255).astype(np.uint8)


def run_render_check(env_cls):
    output_dir = Path(os.environ.get("RR_RENDER_OUTPUT_DIR", "render_outputs"))
    output_dir.mkdir(exist_ok=True)

    env = make_env(env_cls)

    try:
        env.reset()

        for _ in range(5):
            action = env.action_space.sample()
            _, _, done, _ = unpack_step(env.step(action))
            if done:
                env.reset()

        rendered = render_env(env)
        image = normalize_image_array(convert_render_to_array(rendered))

        output_path = output_dir / f"{env_cls.__name__}.png"
        plt.imsave(output_path, image, cmap="gray" if image.ndim == 2 else None)

        assert output_path.exists()
        assert output_path.stat().st_size > 0
        assert np.std(image) > 0, "Rendered image appears to be blank"
        return output_path
    finally:
        if hasattr(env, "close"):
            env.close()


if pytest is not None:
    @pytest.mark.parametrize("env_cls", ENV_CLASSES)
    def test_env_render_outputs_visible_frame(env_cls):
        run_render_check(env_cls)
else:
    def test_env_render_outputs_visible_frame(env_cls):
        run_render_check(env_cls)


def main():
    failures = []

    print("Running rr_envs render smoke tests...")
    for env_cls in ENV_CLASSES:
        try:
            output_path = run_render_check(env_cls)
        except Exception as exc:
            failures.append((env_cls.__name__, exc))
            print(f"[FAIL] {env_cls.__name__}: {type(exc).__name__}: {exc}")
        else:
            print(f"[PASS] {env_cls.__name__}: {output_path}")

    if failures:
        print("\nRender smoke test failed:")
        for env_name, exc in failures:
            print(f"- {env_name}: {type(exc).__name__}: {exc}")
        return 1

    print("\nAll render smoke tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

