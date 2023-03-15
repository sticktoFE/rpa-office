from inspect import isclass, isfunction, ismethod
import sys
import time
import traceback
from PySide6.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal, Slot
from PySide6.QtWidgets import QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
from myutils.LazyImport import lazy_import


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        tuple (exctype, value, traceback.format_exc() )
    result
        object data returned from processing, anything
    progress
        int indicating % progress
    """

    finished = Signal(int)
    error = Signal(tuple)
    fn_result = Signal(tuple)
    # 这是线程处理结果，其实也是执行的fn结果，暂时先留着，后面都用fn_result
    result = Signal(object)
    progress = Signal(int)
    thread_stop = Signal()
    """
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                    kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    重要事说三遍，只有run中代码是运行在子线程中的，不要在init中有耗时的代码，要放到run中
    """


class Worker(QRunnable):
    def __init__(
        self,
        fnOrClass,
        *args,
        classMethod=None,
        classMethodArgs: dict = None,
        classSignal=None,
        need_progress_signal=False,
        module=None,
        **kwargs,
    ):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        # print(f'init {fn} thread name: {QThread.currentThread()}')
        self.fn = fnOrClass
        self.class_method = classMethod
        self.classMethodArgs = classMethodArgs
        self.classSignal = classSignal
        self.module = module
        self.args = args
        self.kwargs = kwargs
        self.communication = WorkerSignals()
        # Add the callback to our kwargs
        # The old way (hard-code the callback to kwargs)
        if need_progress_signal:
            self.kwargs["progress_signal"] = self.communication.progress

    @Slot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        # print(f'run {self.fn} thread name: {QThread.currentThread()}')
        if isinstance(self.fn, str):
            self.fn = lazy_import.getRes(self.module, self.fn)
        fn_result = None
        try:
            # 直接传进 函数或类方法对象
            if isfunction(self.fn) or ismethod(self.fn):
                fn_result = self.fn(*self.args, **self.kwargs)
            # 传进class，如果有方法传进字符串形式的方法名，适用于引进类，然后直接调用类方法
            # 实例化类
            elif isclass(self.fn):
                fn_result = self.fn(*self.args, **self.kwargs)
                if self.class_method is not None:
                    cm = getattr(fn_result, self.class_method)
                    if self.classSignal is not None:

                        def sigal_r(result):
                            self.communication.result.emit(result)

                        _signal = getattr(fn_result, self.classSignal)
                        _signal.connect(sigal_r)
                        cm(**self.classMethodArgs)
                    else:
                        fn_result = cm(**self.classMethodArgs)

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.communication.error.emit((exctype, value, traceback.format_exc()))
        else:
            if self.classSignal is None:
                self.communication.result.emit(fn_result)
        finally:
            self.communication.finished.emit(1)  # Done


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.counter = 0
        layout = QVBoxLayout()
        self.l = QLabel("Start")
        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)
        layout.addWidget(self.l)
        layout.addWidget(b)
        w = QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.show()
        self.threadpool = QThreadPool()
        print(
            "Multithreading with maximum %d threads" % self.threadpool.maxThreadCount()
        )
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(5):
            time.sleep(1)
            progress_callback.emit(n * 100 / 4)
        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        # Any other args, kwargs are passed to the run function
        worker = Worker(self.execute_this_fn)
        worker.communication.result.connect(self.print_output)
        worker.communication.finished.connect(self.thread_complete)
        worker.communication.progress.connect(self.progress_fn)
        # Execute
        self.threadpool.start(worker)

    def recurring_timer(self):
        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)


# app = QApplication(sys.argv)
# window = MainWindow()
# app.exec_()
