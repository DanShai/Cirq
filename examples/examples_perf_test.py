import cirq
import examples.bell_inequality
import examples.bernstein_vazirani
import examples.grover
import examples.place_on_bristlecone
import examples.hello_qubit
import examples.quantum_fourier_transform
import examples.bcs_mean_field
import examples.phase_estimator
import examples.basic_arithmetic


def test_example_runs_bernstein_vazirani_perf(benchmark):
    benchmark(examples.bernstein_vazirani.main, qubit_count=3)

    # Check empty oracle case. Cover both biases.
    a = cirq.NamedQubit('a')
    assert list(examples.bernstein_vazirani.make_oracle(
        [], a, [], False)) == []
    assert list(examples.bernstein_vazirani.make_oracle(
        [], a, [], True)) == [cirq.X(a)]


def test_example_runs_hello_line_perf(benchmark):
    benchmark(examples.place_on_bristlecone.main)


def test_example_runs_hello_qubit_perf(benchmark):
    benchmark(examples.hello_qubit.main)


def test_example_runs_bell_inequality_perf(benchmark):
    benchmark(examples.bell_inequality.main)


def test_example_runs_quantum_fourier_transform_perf(benchmark):
    benchmark(examples.quantum_fourier_transform.main)


def test_example_runs_bcs_mean_field_perf(benchmark):
    benchmark(examples.bcs_mean_field.main)


def test_example_runs_grover_perf(benchmark):
    benchmark(examples.grover.main)


def test_example_runs_phase_estimator_perf(benchmark):
    benchmark(examples.phase_estimator.main, qnums=(2,), repetitions=2)
