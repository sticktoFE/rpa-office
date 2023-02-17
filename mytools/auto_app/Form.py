/********************************************************************************
** Form generated from reading UI file 'Form.ui'
**
** Created by: Qt User Interface Compiler version 6.4.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef FORM_H
#define FORM_H

#include <ImageLabel>
#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QTreeWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Form
{
public:
    QWidget *centralwidget;
    QHBoxLayout *horizontalLayout_2;
    QVBoxLayout *verticalLayout_2;
    QGridLayout *gridLayout;
    QPushButton *getScreenShotPushButton;
    QPushButton *autoClickScreenShot;
    QPushButton *returnHomePushButton;
    QPushButton *returnPushButton;
    QPushButton *recordActionPushButton;
    QPushButton *actionStartPushButton;
    QPushButton *taskStopPushButton;
    QWidget *actionLoadWidget;
    QVBoxLayout *verticalLayout;
    QHBoxLayout *horizontalLayout;
    QPushButton *fileAddPushButton;
    QPushButton *fileRemovePushButton;
    QTreeWidget *taskTreeWidget;
    ImageLabel *screenLabel;

    void setupUi(QMainWindow *Form)
    {
        if (Form->objectName().isEmpty())
            Form->setObjectName("Form");
        Form->resize(418, 412);
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(Form->sizePolicy().hasHeightForWidth());
        Form->setSizePolicy(sizePolicy);
        centralwidget = new QWidget(Form);
        centralwidget->setObjectName("centralwidget");
        horizontalLayout_2 = new QHBoxLayout(centralwidget);
        horizontalLayout_2->setSpacing(3);
        horizontalLayout_2->setObjectName("horizontalLayout_2");
        horizontalLayout_2->setContentsMargins(0, 0, 0, 0);
        verticalLayout_2 = new QVBoxLayout();
        verticalLayout_2->setObjectName("verticalLayout_2");
        gridLayout = new QGridLayout();
        gridLayout->setObjectName("gridLayout");
        getScreenShotPushButton = new QPushButton(centralwidget);
        getScreenShotPushButton->setObjectName("getScreenShotPushButton");
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Fixed);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(getScreenShotPushButton->sizePolicy().hasHeightForWidth());
        getScreenShotPushButton->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(getScreenShotPushButton, 0, 0, 1, 1);

        autoClickScreenShot = new QPushButton(centralwidget);
        autoClickScreenShot->setObjectName("autoClickScreenShot");
        sizePolicy1.setHeightForWidth(autoClickScreenShot->sizePolicy().hasHeightForWidth());
        autoClickScreenShot->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(autoClickScreenShot, 0, 1, 1, 1);

        returnHomePushButton = new QPushButton(centralwidget);
        returnHomePushButton->setObjectName("returnHomePushButton");
        sizePolicy1.setHeightForWidth(returnHomePushButton->sizePolicy().hasHeightForWidth());
        returnHomePushButton->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(returnHomePushButton, 1, 0, 1, 1);

        returnPushButton = new QPushButton(centralwidget);
        returnPushButton->setObjectName("returnPushButton");
        sizePolicy1.setHeightForWidth(returnPushButton->sizePolicy().hasHeightForWidth());
        returnPushButton->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(returnPushButton, 1, 1, 1, 1);

        recordActionPushButton = new QPushButton(centralwidget);
        recordActionPushButton->setObjectName("recordActionPushButton");
        sizePolicy1.setHeightForWidth(recordActionPushButton->sizePolicy().hasHeightForWidth());
        recordActionPushButton->setSizePolicy(sizePolicy1);
        recordActionPushButton->setCheckable(true);
        recordActionPushButton->setChecked(true);

        gridLayout->addWidget(recordActionPushButton, 2, 0, 1, 1);

        actionStartPushButton = new QPushButton(centralwidget);
        actionStartPushButton->setObjectName("actionStartPushButton");
        sizePolicy1.setHeightForWidth(actionStartPushButton->sizePolicy().hasHeightForWidth());
        actionStartPushButton->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(actionStartPushButton, 3, 0, 1, 1);

        taskStopPushButton = new QPushButton(centralwidget);
        taskStopPushButton->setObjectName("taskStopPushButton");
        sizePolicy1.setHeightForWidth(taskStopPushButton->sizePolicy().hasHeightForWidth());
        taskStopPushButton->setSizePolicy(sizePolicy1);

        gridLayout->addWidget(taskStopPushButton, 3, 1, 1, 1);


        verticalLayout_2->addLayout(gridLayout);

        actionLoadWidget = new QWidget(centralwidget);
        actionLoadWidget->setObjectName("actionLoadWidget");
        verticalLayout = new QVBoxLayout(actionLoadWidget);
        verticalLayout->setObjectName("verticalLayout");
        horizontalLayout = new QHBoxLayout();
        horizontalLayout->setObjectName("horizontalLayout");
        fileAddPushButton = new QPushButton(actionLoadWidget);
        fileAddPushButton->setObjectName("fileAddPushButton");
        sizePolicy1.setHeightForWidth(fileAddPushButton->sizePolicy().hasHeightForWidth());
        fileAddPushButton->setSizePolicy(sizePolicy1);

        horizontalLayout->addWidget(fileAddPushButton);

        fileRemovePushButton = new QPushButton(actionLoadWidget);
        fileRemovePushButton->setObjectName("fileRemovePushButton");
        sizePolicy1.setHeightForWidth(fileRemovePushButton->sizePolicy().hasHeightForWidth());
        fileRemovePushButton->setSizePolicy(sizePolicy1);

        horizontalLayout->addWidget(fileRemovePushButton);


        verticalLayout->addLayout(horizontalLayout);

        taskTreeWidget = new QTreeWidget(actionLoadWidget);
        taskTreeWidget->headerItem()->setText(1, QString());
        taskTreeWidget->setObjectName("taskTreeWidget");
        sizePolicy.setHeightForWidth(taskTreeWidget->sizePolicy().hasHeightForWidth());
        taskTreeWidget->setSizePolicy(sizePolicy);

        verticalLayout->addWidget(taskTreeWidget);


        verticalLayout_2->addWidget(actionLoadWidget);

        verticalLayout_2->setStretch(0, 3);
        verticalLayout_2->setStretch(1, 7);

        horizontalLayout_2->addLayout(verticalLayout_2);

        screenLabel = new ImageLabel(centralwidget);
        screenLabel->setObjectName("screenLabel");
        QSizePolicy sizePolicy2(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy2.setHorizontalStretch(204);
        sizePolicy2.setVerticalStretch(115);
        sizePolicy2.setHeightForWidth(screenLabel->sizePolicy().hasHeightForWidth());
        screenLabel->setSizePolicy(sizePolicy2);
        screenLabel->setMouseTracking(true);
        screenLabel->setTabletTracking(true);
        screenLabel->setAcceptDrops(false);
        screenLabel->setAutoFillBackground(false);
        screenLabel->setStyleSheet(QString::fromUtf8(""));
        screenLabel->setScaledContents(true);
        screenLabel->setAlignment(Qt::AlignCenter);
        screenLabel->setWordWrap(false);

        horizontalLayout_2->addWidget(screenLabel);

        horizontalLayout_2->setStretch(0, 2);
        horizontalLayout_2->setStretch(1, 8);
        Form->setCentralWidget(centralwidget);

        retranslateUi(Form);

        QMetaObject::connectSlotsByName(Form);
    } // setupUi

    void retranslateUi(QMainWindow *Form)
    {
        Form->setWindowTitle(QCoreApplication::translate("Form", "auto_mobile", nullptr));
        getScreenShotPushButton->setText(QCoreApplication::translate("Form", "\350\216\267\345\217\226\345\261\217\345\271\225", nullptr));
        autoClickScreenShot->setText(QCoreApplication::translate("Form", "\345\220\257\345\212\250\344\273\273\345\212\241", nullptr));
        returnHomePushButton->setText(QCoreApplication::translate("Form", "\350\277\224\345\233\236\346\241\214\351\235\242", nullptr));
        returnPushButton->setText(QCoreApplication::translate("Form", "\350\277\224\345\233\236\344\270\212\344\270\200\347\272\247", nullptr));
        recordActionPushButton->setText(QCoreApplication::translate("Form", "\345\274\200\345\247\213\345\275\225\345\210\266\345\212\250\344\275\234", nullptr));
        actionStartPushButton->setText(QCoreApplication::translate("Form", "\345\274\200\345\247\213\346\211\247\350\241\214", nullptr));
        taskStopPushButton->setText(QCoreApplication::translate("Form", "\344\273\273\345\212\241\347\273\210\346\255\242", nullptr));
        fileAddPushButton->setText(QCoreApplication::translate("Form", "\346\267\273\345\212\240", nullptr));
        fileRemovePushButton->setText(QCoreApplication::translate("Form", "\347\247\273\351\231\244", nullptr));
        QTreeWidgetItem *___qtreewidgetitem = taskTreeWidget->headerItem();
        ___qtreewidgetitem->setText(0, QCoreApplication::translate("Form", "\344\273\273\345\212\241\345\210\227\350\241\250", nullptr));
        screenLabel->setText(QCoreApplication::translate("Form", "\345\233\276\347\211\207\346\230\276\347\244\272\345\214\272\345\237\237", nullptr));
    } // retranslateUi

};

namespace Ui {
    class Form: public Ui_Form {};
} // namespace Ui

QT_END_NAMESPACE

#endif // FORM_H
