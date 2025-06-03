<template>
  <div class="chat-wrapper">
    <!-- Gornji dio: prikaz poruka -->
    <div class="chat-log">
      <div v-for="(line, index) in messages" :key="index">
        {{ line }}
      </div>
    </div>

    <!-- Donji dio: unos poruke -->
    <div class="chat-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="Type here..."
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const messages = ref(["Welcome to Chat Room"]);
const newMessage = ref("");
let username = "";

// Traži korisnika pri ulasku
onMounted(() => {
  while (!username) {
    username = prompt("Enter your username:");
  }
  messages.value.push(`${username} joined`);
});

// Funkcija za slanje poruke
function sendMessage() {
  if (!newMessage.value) return;
  messages.value.push(`${username}: ${newMessage.value}`);
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
  border-top: 2px solid black;
  padding: 5px;
}

.chat-input input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: none;
}
</style>
