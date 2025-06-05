<template>
  <div class="chat-wrapper">
    <div class="chat-log">
      <div v-for="(line, index) in messages" :key="index">
        {{ line }}
      </div>
    </div>

    <div class="chat-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="Upiši poruku..."
      />
      <button @click="sendMessage">Pošalji</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const messages = ref(["Dobrodošao u Chat sobu"]);
const newMessage = ref("");
let username = "";
const socket = ref(null);

// Pita korisnika za ime
onMounted(() => {
  while (!username) {
    username = prompt("Upiši svoje ime:");
  }

  socket.value = new WebSocket("ws://localhost:8000/ws");

  socket.value.onopen = () => {
    socket.value.send(
      JSON.stringify({
        username: username,
        message: "__joined__",
      })
    );
  };

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data);
    socket.value.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.message === "__joined__") {
        messages.value.push(`${data.username} se pridružio Chat-u`);
      } else {
        messages.value.push(`${data.username}: ${data.message}`);
      }
    };
  };

  socket.value.onclose = () => {
    messages.value.push("🔌 Veza prekinuta");
  };
});

function sendMessage() {
  if (!newMessage.value || !socket.value) return;

  const msg = {
    username: username,
    message: newMessage.value,
  };

  socket.value.send(JSON.stringify(msg));
  newMessage.value = "";
}
</script>

<style scoped>
.chat-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #ddd;
  font-family: monospace;
}

.chat-log {
  flex-grow: 1;
  padding: 10px;
  overflow-y: auto;
}

.chat-input {
  padding: 10px;
  display: flex;
  gap: 10px;
  background: #fff;
}

.chat-input input {
  flex: 1;
  padding: 10px 15px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 999px;
  outline: none;
}

.chat-input button {
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  background-color: #000;
  color: #fff;
  border-radius: 999px; /* Zaobljeni rubovi */
  cursor: pointer;
  transition: background-color 0.2s;
}

.chat-input button:hover {
  background-color: #333;
}
</style>
