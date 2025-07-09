import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Login from "../Login";
import { BrowserRouter } from "react-router-dom";

// Mock useNavigate (¡fuera del test!)
const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
}));

// Mock de contexto de lenguaje
jest.mock("../../lenguage/LenguageContext", () => ({
  useLanguage: () => ({
    translations: {
      loginTitle: "Iniciar Sesión",
      emailPlaceholder: "Correo electrónico",
      loginPlaceholder: "Contraseña",
      loginButton: "Entrar",
      loginError: "Correo o contraseña incorrectos",
    },
  }),
}));

// Mock del componente Boton
jest.mock("../Button", () => (props: any) => (
  <button onClick={props.onClick || (() => {})} type={props.type}>
    {props.texto}
  </button>
));

describe("Login Component", () => {
  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  test("renderiza el formulario de login", () => {
    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );
    expect(screen.getByPlaceholderText("Correo electrónico")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Contraseña")).toBeInTheDocument();
    expect(screen.getByText("Entrar")).toBeInTheDocument();
  });

  test("muestra error si las credenciales son incorrectas", async () => {
    global.fetch = jest.fn(() => Promise.resolve({ status: 401 })) as jest.Mock;

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Correo electrónico"), {
      target: { value: "user@test.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
      target: { value: "wrongpass" },
    });

    fireEvent.click(screen.getByText("Entrar"));

    await waitFor(() =>
      expect(screen.getByText("Correo o contraseña incorrectos")).toBeInTheDocument()
    );
  });

  test("redirige si las credenciales son correctas", async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        status: 200,
        json: () => Promise.resolve({ token: "abc123" }),
      })
    ) as jest.Mock;

    render(
      <BrowserRouter>
        <Login />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByPlaceholderText("Correo electrónico"), {
      target: { value: "admin@test.com" },
    });
    fireEvent.change(screen.getByPlaceholderText("Contraseña"), {
      target: { value: "123456" },
    });

    fireEvent.click(screen.getByText("Entrar"));

    await waitFor(() => expect(localStorage.getItem("token")).toBe("abc123"));
    expect(mockNavigate).toHaveBeenCalledWith("/admin-dashboard");
  });
});
