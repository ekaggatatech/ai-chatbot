// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore} from "firebase/firestore";
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCRUl6TwpX3JEAWQcDKz38iNTQJB9K4ObU",
  authDomain: "test-cfae7.firebaseapp.com",
  projectId: "test-cfae7",
  storageBucket: "test-cfae7.firebasestorage.app",
  messagingSenderId: "191580878530",
  appId: "1:191580878530:web:d7900afc57c683400dad5b",
  measurementId: "G-HX9EWE2NTT"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Intialize Firestore and export it
export const db=getFirestore(app);
export default app;