async function parseErrorDetail(res, fallback) {
  try {
    const body = await res.json();
    return body.detail || fallback;
  } catch {
    return fallback;
  }
}

export async function register(email, password) {
  const res = await fetch("/api/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error(await parseErrorDetail(res, "Could not create an account"));
  return res.json();
}

export async function login(email, password) {
  const res = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error(await parseErrorDetail(res, "Invalid email or password"));
  return res.json();
}

export async function logout() {
  await fetch("/api/auth/logout", { method: "POST" });
}

export async function me() {
  const res = await fetch("/api/auth/me");
  if (!res.ok) return null;
  return res.json();
}

export async function listVideos() {
  const res = await fetch("/api/videos");
  if (!res.ok) throw new Error("Failed to load videos");
  return res.json();
}

export async function askQuestion(videoId, question) {
  const res = await fetch(`/api/videos/${videoId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error("Failed to get an answer");
  return res.json();
}
