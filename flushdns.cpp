#include <QApplication>
#include <QPushButton>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QLabel>
#include <QTimer>
#include <QProcess>
#include <QDateTime>

class MainWindow : public QWidget {
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr)
        : QWidget(parent), isRunning(false), flushedCount(0), cooldown(60) {
        QVBoxLayout *layout = new QVBoxLayout(this);

        logBox = new QTextEdit(this);
        logBox->setReadOnly(true);
        layout->addWidget(logBox);

        statusLabel = new QLabel("Status: Idle", this);
        layout->addWidget(statusLabel);

        QPushButton *startButton = new QPushButton("Start", this);
        connect(startButton, &QPushButton::clicked, this, &MainWindow::startFlush);
        layout->addWidget(startButton);

        QPushButton *stopButton = new QPushButton("Stop", this);
        connect(stopButton, &QPushButton::clicked, this, &MainWindow::stopFlush);
        layout->addWidget(stopButton);

        timer = new QTimer(this);
        connect(timer, &QTimer::timeout, this, &MainWindow::flushDNS);
    }

public slots:
    void startFlush() {
        if (!isRunning) {
            isRunning = true;
            log("Starting script");
            statusLabel->setText("Status: Starting script");
            timer->start(1000); // Call flushDNS every 1 second
        }
    }

    void stopFlush() {
        if (isRunning) {
            isRunning = false;
            timer->stop();
            log("Stopping script");
            statusLabel->setText("Status: Stopping script");
        }
    }

    void flushDNS() {
        if (isRunning && cooldown <= 0) {
            QProcess::execute("ipconfig /flushdns");
            flushedCount++;
            log("Flushing DNS. FLUSHED " + QString::number(flushedCount) + " times");
            statusLabel->setText("Status: Flushing DNS, please wait...");
            cooldown = 60;
        } else if (isRunning) {
            cooldown--;
            statusLabel->setText("Status: Flushed DNS, cooldown " + QString::number(cooldown) + " seconds");
        }
    }

private:
    void log(const QString &message) {
        logBox->append(QDateTime::currentDateTime().toString("[hh:mm:ss] ") + message);
    }

    QTextEdit *logBox;
    QLabel *statusLabel;
    QTimer *timer;
    bool isRunning;
    int flushedCount;
    int cooldown;
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    MainWindow window;
    window.show();

    return app.exec();
}

#include "main.moc"