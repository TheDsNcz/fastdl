// Configuração do Firebase - substitua pelos seus dados!
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "SENDER_ID",
  appId: "APP_ID",
};

// Inicializar Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

const postForm = document.getElementById("post-form");
const postsContainer = document.getElementById("posts-container");

// Adiciona nova postagem
postForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("title").value.trim();
  const content = document.getElementById("content").value.trim();

  if (!title || !content) return;

  await db.collection("posts").add({
    title,
    content,
    createdAt: firebase.firestore.FieldValue.serverTimestamp(),
  });

  postForm.reset();
});

// Renderiza postagens em tempo real
function renderPost(doc) {
  const data = doc.data();
  const card = document.createElement("div");
  card.className = "card shadow-sm";

  const cardBody = document.createElement("div");
  cardBody.className = "card-body";

  const h5 = document.createElement("h5");
  h5.className = "card-title";
  h5.textContent = data.title;

  const p = document.createElement("p");
  p.className = "card-text";
  p.textContent = data.content;

  const small = document.createElement("small");
  small.className = "text-muted";
  const date = data.createdAt ? data.createdAt.toDate().toLocaleString() : "";
  small.textContent = date;

  cardBody.appendChild(h5);
  cardBody.appendChild(p);
  cardBody.appendChild(small);
  card.appendChild(cardBody);
  postsContainer.prepend(card);
}

// Escuta alterações

db.collection("posts")
  .orderBy("createdAt", "desc")
  .onSnapshot((snapshot) => {
    postsContainer.innerHTML = "";
    snapshot.forEach((doc) => renderPost(doc));
  });