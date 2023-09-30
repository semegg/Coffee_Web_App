let tg = window.Telegram.WebApp;
tg.expand();
tg.MainButton.textColor = "#FFFFFF";
tg.MainButton.color = "#2cab37";

let items = [];

const savedItems = localStorage.getItem("items");
if (savedItems) {
  items = JSON.parse(savedItems);
  if (window.location.pathname === "/") {
    tg.MainButton.setText("Continue");
  } else {
    const count = items.length;
    tg.MainButton.setText(`Вы выбрали ${count} товаров !`);
  }
  tg.MainButton.show();
}


Telegram.WebApp.onEvent("mainButtonClicked", function() {
  if (window.location.pathname === "/") {
    tg.sendData(savedItems);
    localStorage.clear();
} else if (window.location.pathname === "/menu.html") {
    localStorage.setItem("items", JSON.stringify(items));
    window.location.href = "/";
  }
});




let buttons = document.querySelectorAll('[id^="btn_"]');
buttons.forEach(button => {
  button.addEventListener("click", function() {
    const buttonId = button.id.slice(4);
    items.push(buttonId);
    const count = items.length;
    tg.MainButton.setText(`Вы выбрали ${count} товаров !`);
    tg.MainButton.show();
  });
});

let removeButtons = document.querySelectorAll('[id^="remove_"]');
removeButtons.forEach(button => {
  button.addEventListener("click", function() {
    const buttonId = button.id.slice(7); // Видаляємо префікс "remove_" з ідентифікатора
    const index = items.indexOf(buttonId);

    if (index !== -1) {
      items.splice(index, 1); // Видаляємо елемент з масиву за індексом
    }

    const count = items.length;
    tg.MainButton.setText(`Вы выбрали ${count} товаров!`);
    tg.MainButton.show();


    if (count === 0) {
      tg.MainButton.hide(); // Ховаємо кнопку, якщо масив порожній
    }
  });
});


const itemsElements = document.body.getElementsByClassName("item");
for (let item of Array.from(itemsElements)) {
  const counter = item.getElementsByClassName("counter")[0];
  counter.style.setProperty("visibility", "hidden");

  const table = item.getElementsByClassName("table")[0];
  table.style.setProperty("display", "none");
  const row = table.getElementsByClassName("row")[0];

  const inc = row.getElementsByClassName("plus")[0];
  inc.addEventListener("click", () => increment(item));

  const dec = row.getElementsByClassName("minus")[0];
  dec.addEventListener("click", () => decrement(item));

  const add = item.getElementsByClassName("add")[0];
  add.addEventListener("click", () => increment(item));

  const initialValue = localStorage.getItem(`counter_${item.id}`);

  if (initialValue > 0) {
    counter.style.setProperty("visibility", "visible");
    counter.textContent = Number(initialValue);
    item.getElementsByClassName("table")[0].style.setProperty("display", "block");
    item.getElementsByClassName("add")[0].style.setProperty("display", "none");
  }
}

const increment = (item) => {
  const counter = item.getElementsByClassName("counter")[0];
  let value = Number(counter.textContent);

  if (!value) {
    counter.style.setProperty("visibility", "visible");
    item.getElementsByClassName("table")[0].style.setProperty("display", "block");
    item.getElementsByClassName("add")[0].style.setProperty("display", "none");
  }

  value += 1;
  counter.textContent = value;
  localStorage.setItem(`counter_${item.id}`, value);
};

const decrement = (item) => {
  const counter = item.getElementsByClassName("counter")[0];
  let value = Number(counter.textContent);

  if (!(value - 1)) {
    counter.style.setProperty("visibility", "hidden");
    item.getElementsByClassName("table")[0].style.setProperty("display", "none");
    item.getElementsByClassName("add")[0].style.setProperty("display", "block");
  }

  value -= 1;
  counter.textContent = value;
  localStorage.setItem(`counter_${item.id}`, value);
};