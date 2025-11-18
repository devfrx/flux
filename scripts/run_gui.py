"""Avvia la GUI desktop di Flux Agent."""
from flux_agent.gui import FluxAgentApp


def main():
    app = FluxAgentApp()
    app.run()


if __name__ == "__main__":
    main()