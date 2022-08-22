import time
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour, OneShotBehaviour, FSMBehaviour, State
from spade.message import Message


class SumAgent(Agent):
    class ReceiveMsg(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=0)
            if msg:
                msg = Message(to="coordinator_agent@localhost/5222")
                msg.body = str(num1 + num2)
                await self.send(msg)

    async def setup(self):
        print("SumAgent starting . . .")
        self.add_behaviour(self.ReceiveMsg())


class SubtractionAgent(Agent):
    class ReceiveMsg(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=0)
            if msg:
                print("Expressao de subtracao recebida")  # faz alguma coisa com a mensagem

    async def setup(self):
        print("SubtractionAgent starting . . .")
        self.add_behaviour(self.ReceiveMsg())


class MultiplicationAgent(Agent):
    class ReceiveMsg(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=0)
            if msg:
                print("Expressao de multiplicacao recebida")  # faz alguma coisa com a mensagem

    async def setup(self):
        print("MultiplicationAgent starting . . .")
        self.add_behaviour(self.ReceiveMsg())


class DivisionAgent(Agent):
    class ReceiveMsg(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=0)
            if msg:
                print("Expressao de divisao recebida")  # faz alguma coisa com a mensagem

    async def setup(self):
        print("DivisionAgent starting . . .")
        self.add_behaviour(self.ReceiveMsg())


class PowerAgent(Agent):
    class ReceiveMsg(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                print("Expressao recebida")  # faz alguma coisa com a mensagem

    async def setup(self):
        print("PowerAgent starting . . .")
        self.add_behaviour(self.ReceiveMsg())


class SquareRootAgent(Agent):
    class ReceiveMsg(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                print("Expressao recebida")  # faz alguma coisa com a mensagem

        async def on_end(self):
            pass

    async def setup(self):
        print("Agent starting . . .")
        self.add_behaviour(self.ReceiveMsg())


class CoordinatorAgent(Agent):
    class WaitMsg(State):
        async def run(self):
            print('Coordenador: esperando mensagens')
            msg = await self.receive(timeout=5)
            if msg:
                time.sleep(1)
                print(f"Coordenador: mensagem recebida {msg.body}")
                msg = Message(to='initializer_agent@localhost/5222')
                msg.body = 'resposta'
                print('Coordenador: Resposta ao inicializador enviada')
                await self.send(msg)
                self.set_next_state('REQUEST_SUM')
            elif msg == '2':
                msg = Message(to='subtract_agent@localhost/5222')
                msg.body = 'resposta'
                await self.send(msg)
                self.set_next_state('REQUEST_SUBTRACTION')
            elif msg == '3':
                msg = Message(to='multiplication_agent@localhost/5222')
                msg.body = 'resposta'
                await self.send(msg)
                self.set_next_state('REQUEST_MULTIPLICATION')
            elif msg == '3':
                msg = Message(to='division_agent@localhost/5222')
                msg.body = 'resposta'
                await self.send(msg)
                self.set_next_state('REQUEST_DIVISION')
            elif msg == '4':
                msg = Message(to='power_agent@localhost/5222')
                msg.body = 'resposta'
                await self.send(msg)
                self.set_next_state('REQUEST_POWER')
            elif msg == '5':
                msg = Message(to='squareroot_agent@localhost/5222')
                msg.body = 'resposta'
                await self.send(msg)
                self.set_next_state('REQUEST_SQUAREROOT')
            else:
                time.sleep(1)
                print('Coordenador: nenhuma mensagem recebida')
                self.set_next_state('WAIT_MSG')

    class RequestSum(State):
        async def run(self):
            time.sleep(1)
            msg = Message(to='sum_agent@localhost/5222')
            msg.body = 'Operação recebida, o resultado foi esse'

            await self.send(msg)

            self.set_next_state('WAIT_MSG')

    class RequestSubtraction(State):
        async def run(self):
            time.sleep(1)
            msg = Message(to='subtract_agent@localhost/5222')
            msg.body = 'Operação recebida, o resultado foi esse'

            await self.send(msg)

            self.set_next_state('WAIT_MSG')

    class RequestMultiplication(State):
        async def run(self):
            time.sleep(1)
            msg = Message(to='multiplication_agent@localhost/5222')
            msg.body = 'Operação recebida, o resultado foi esse'

            await self.send(msg)

            self.set_next_state('WAIT_MSG')

    class RequestDivision(State):
        async def run(self):
            time.sleep(1)
            msg = Message(to='division_agent@localhost/5222')
            msg.body = 'Operação recebida, o resultado foi esse'

            await self.send(msg)

            self.set_next_state('WAIT_MSG')

    class RequestPower(State):
        async def run(self):
            time.sleep(1)
            msg = Message(to='power_agent@localhost/5222')
            msg.body = 'Operação recebida, o resultado foi esse'

            await self.send(msg)

            self.set_next_state('WAIT_MSG')

    class RequestSquareRoot(State):
        async def run(self):
            time.sleep(1)
            msg = Message(to='squareroot_agent@localhost/5222')
            msg.body = 'Operação recebida, o resultado foi esse'

            await self.send(msg)

            self.set_next_state('WAIT_MSG')

    async def setup(self):
        print("Coordinator_agent starting . . .")
        fsm = FSMBehaviour()
        fsm.add_state(name='WAIT_MSG', state=self.WaitMsg(), initial=True)
        fsm.add_state(name='REQUEST_SUM', state=self.RequestSum())
        fsm.add_state(name='REQUEST_SUBTRACTION', state=self.RequestSubtraction())
        fsm.add_state(name='REQUEST_MULTIPLICATION', state=self.RequestMultiplication())
        fsm.add_state(name='REQUEST_DIVISION', state=self.RequestDivision())
        fsm.add_state(name='REQUEST_POWER', state=self.RequestPower())
        fsm.add_state(name='REQUEST_SQUAREROOT', state=self.RequestSquareRoot())
        fsm.add_transition(source='WAIT_MSG', dest='REQUEST_SUM')
        fsm.add_transition(source='WAIT_MSG', dest='REQUEST_SUBTRACTION')
        fsm.add_transition(source='WAIT_MSG', dest='REQUEST_MULTIPLICATION')
        fsm.add_transition(source='WAIT_MSG', dest='REQUEST_DIVISION')
        fsm.add_transition(source='WAIT_MSG', dest='REQUEST_POWER')
        fsm.add_transition(source='WAIT_MSG', dest='REQUEST_SQUAREROOT')
        fsm.add_transition(source='REQUEST_SUM', dest='WAIT_MSG')
        fsm.add_transition(source='REQUEST_SUBTRACTION', dest='WAIT_MSG')
        fsm.add_transition(source='REQUEST_MULTIPLICATION', dest='WAIT_MSG')
        fsm.add_transition(source='REQUEST_DIVISION', dest='WAIT_MSG')
        fsm.add_transition(source='REQUEST_POWER', dest='WAIT_MSG')
        fsm.add_transition(source='REQUEST_SQUAREROOT', dest='WAIT_MSG')
        fsm.add_transition(source='WAIT_MSG', dest='WAIT_MSG')
        self.add_behaviour(fsm)


class IntializerAgent(Agent):
    class GetExpression(State):
        async def run(self):
            expression = input('Digite a expressão a ser calculada: ')
            expression = expression.split(" ")
            self.set_next_state('CALL_COORDINATOR')

    class RecvAnswer(State):
        async def run(self):
            time.sleep(1)
            print('Inicializador: esperando resposta do coordenador')
            msg = await self.receive(timeout=5)
            if msg:
                time.sleep(1)
                print('Inicializador: reposta do coordenador recebida')  # faz alguma coisa com a mensagem
                self.set_next_state('CALL_COORDINATOR')
            else:
                time.sleep(1)
                print('Inicializador: nenhuma resposta recebida')
                self.set_next_state('CALL_COORDINATOR')

    class CallCoordinator(State):
        async def run(self):
            time.sleep(5)
            print('Inicializador: chamando coordenador')
            msg = Message(to="coordinator_agent@localhost/5222")
            msg.body = "expressao a ser calculada"
            await self.send(msg)
            self.set_next_state('RECEIVE_ANSWER')

    async def setup(self):
        print("Initializer_agent starting . . .")
        fsm = FSMBehaviour()
        fsm.add_state(name='GET_EXPRESSION', state=self.GetExpression(), initial=True)
        fsm.add_state(name='CALL_COORDINATOR', state=self.CallCoordinator())
        fsm.add_state(name='RECEIVE_ANSWER', state=self.RecvAnswer())
        fsm.add_transition('GET_EXPRESSION', 'CALL_COORDINATOR')
        fsm.add_transition('CALL_COORDINATOR', 'RECEIVE_ANSWER')
        fsm.add_transition('RECEIVE_ANSWER', 'RECEIVE_ANSWER')
        fsm.add_transition('RECEIVE_ANSWER', 'CALL_COORDINATOR')
        self.add_behaviour(fsm)


if __name__ == "__main__":
    soma = SumAgent("sum_agent@localhost/5222", "123")
    future = soma.start()
    future.result()
    subtracao = SubtractionAgent("subtract_agent@localhost/5222", "123")
    future = subtracao.start()
    future.result()
    multiplicacao = MultiplicationAgent("multiplication_agent@localhost/5222", "123")
    future = multiplicacao.start()
    future.result()
    divisao = DivisionAgent("division_agent@localhost/5222", "123")
    future = divisao.start()
    future.result()
    potencia = PowerAgent("power_agent@localhost/5222", "123")
    future = potencia.start()
    future.result()
    raiz = SquareRootAgent("squareroot_agent@localhost/5222", "123")
    future = raiz.start()
    future.result()
    coordenador = CoordinatorAgent("coordinator_agent@localhost/5222", "123")
    future = coordenador.start()
    future.result()
    inicializador = IntializerAgent("initializer_agent@localhost/5222", "123")
    future = inicializador.start()
    future.result()


    while inicializador.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            soma.stop()
            subtracao.stop()
            multiplicacao.stop()
            divisao.stop()
            coordenador.stop()
            inicializador.stop()
            break
    print("Agents finished")
