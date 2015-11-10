{
    NQItemEventKeeper* keeper = NQItemEventKeeper::instance();
    if (!keeper) {
        return false;
    }
    NGTouchEvent* touch = evt.get();
    if (!touch) {
        return false;
    }

    bool forcePress = false;
    bool firstTouchEvent = m_1stTouchEvent;
    m_1stTouchEvent = false;
    if (NG::TouchBegin == touch->type()) {
        printf("NQItem::deliverTouchEvent touch begin !!\n");
        keeper->onNGTouchBegin();
    }
    // send to parent that stolen event
    else if (keeper->isStolenByParent()) {
        printf("NQItem::deliverTouchEvent isStolenByParent !!\n");
        QTouchEvent* event =  NQPadTouchManager::instance()->translateToQTouchEvent(evt, false);
        if (!event) {
            keeper->clear();
            return false;
        }
            
        QQuickItem*  receiver = keeper->getReceiver();
        if (!receiver) {
            keeper->clear();
            delete event;
            return false;
        }
            
        transformTouchPoints(const_cast<QList<QTouchEvent::TouchPoint>&>(event->touchPoints()), receiver);
        outputTouchDeliverLog(this, receiver, event, "NQItem::deliverTouchEvent StolenByParent");
        NQItem *nqtarget = qobject_cast<NQItem*>(receiver);
        // touch point extend data must be updated before sending touch event to item.
        keeper->updateTouchPointExtendData(touch);
        if (nqtarget) {
            QCoreApplication::sendEvent(nqtarget->getPadEventHandler()? nqtarget->getPadEventHandler():nqtarget, event);
        }
        else {
            QCoreApplication::sendEvent(receiver, event);
        }
        keepLastTouchEvent(event);
        return true;
    }
    else {
        if (firstTouchEvent) {
            if (NG::TouchEnd == touch->type() || NG::TouchCancel == touch->type()) {
                return false;
            }
            forcePress = true;
        }
    }

    {
        QQuickWindow *win = window();
        if (!win) {
            return false;
        }
        QQuickWindowPrivate *winPrivate = QQuickWindowPrivate::get(win);
        if (!winPrivate) {
            return false;
        }

        QTouchEvent* event =  NQPadTouchManager::instance()->translateToQTouchEvent(evt, forcePress);
        if (!event) {
            return false;
        }

#ifdef NQTOUCH_NGLOG_OUTPUT
        const QList<QTouchEvent::TouchPoint> &tps = event->touchPoints();
        QList<QTouchEvent::TouchPoint>::const_iterator iter = tps.begin();
        while (iter != tps.end()) {
            printf( "deliverTouchPoints  normal id[%d]state[%d] screenPos[%f,%f][%f,%f][%f,%f] ", 
                iter->id(),
                iter->state(),
    
                iter->screenPos().x(),
                iter->screenPos().y(),
                iter->startScreenPos().x(),
                iter->startScreenPos().y(),
                iter->lastScreenPos().x(),
                iter->lastScreenPos().y()
            );
            ++iter;
        }
#endif

        // send to Filter parent first
        QQuickItem *target =  parentItem();
        while (target) {
            NQItem *nqtarget = qobject_cast<NQItem*>(target);
            if (nqtarget) {
                if (nqtarget->isFiltersChildEvents()) {
                    QQuickItemPrivate *targetPrivate = QQuickItemPrivate::get(target);
                    transformTouchPoints(const_cast<QList<QTouchEvent::TouchPoint>&>(event->touchPoints()), target);
                    if (nqtarget->childEventsFilter(this, event)) {
                        // touch point extend data must be updated before sending touch event to item.
                        keeper->updateTouchPointExtendData(touch);
                        QCoreApplication::sendEvent(nqtarget->getPadEventHandler()? nqtarget->getPadEventHandler():nqtarget, event);
                        if (event->isAccepted()) {
                            onChildEventsFilter(keeper->getReceiver(), nqtarget);
                            keeper->setReceiver(nqtarget);
                            outputTouchDeliverLog(this, target, event, "NQItem::deliverTouchEvent 2");
                            keepLastTouchEvent(event);
                            keeper->setStolenByParent(true);
                            return true;
                        }
                    }
                }
            }
            
            target = target->parentItem();
        }

#if 0
        target =  parentItem();
        // First check whether the parent wants to be a filter,
        // and if the parent accepts the event we are done.
        while (target) {
            QQuickItemPrivate *targetPrivate = QQuickItemPrivate::get(target);
            NQItem *nqtarget = qobject_cast<NQItem*>(target);
            
            if (nqtarget && targetPrivate->filtersChildMouseEvents) {
                transformTouchPoints(const_cast<QList<QTouchEvent::TouchPoint>&>(event->touchPoints()), target);
                QVector<int> touchIds;
                for (int i = 0; i < event->touchPoints().size(); ++i) {
                    touchIds.append(event->touchPoints().at(i).id());
                }
                
                if (nqtarget->childMouseEventFilter(this, event)) {
                    target->grabTouchPoints(touchIds);
                    if (winPrivate->mouseGrabberItem) {
                        winPrivate->mouseGrabberItem->ungrabMouse();
                        winPrivate->touchMouseId = -1;
                    }
    
                    keeper->setReceiver(target);
                    keeper->setStolenByParent(true);
                    keeper->setChildMouseEventFilter(true);
                    outputTouchDeliverLog(this, target, event, "NQItem::deliverTouchEvent for childMouseEventFilter touch");
                    keepLastTouchEvent(event);
                    return true;
                }
    
                QEvent::Type t;
                const QTouchEvent::TouchPoint &tp = event->touchPoints().first();
                switch (tp.state()) {
                case Qt::TouchPointPressed:
                    t = QEvent::MouseButtonPress;
                    break;
                case Qt::TouchPointReleased:
                    t = QEvent::MouseButtonRelease;
                    break;
                default:
                    // move or stationary
                    t = QEvent::MouseMove;
                    break;
                }
                
                // transformed wrt local position, velocity, etc.
                QScopedPointer<QMouseEvent> mouseEvent(touchToMouseEvent(t, event->touchPoints().first(), event, target, false));
                if (nqtarget->childMouseEventFilter(this, mouseEvent.data())) {
                    winPrivate->itemForTouchPointId[tp.id()] = target;
                    winPrivate->touchMouseId = tp.id();
                    target->grabMouse();
                    keeper->setReceiver(target);
                    keeper->setStolenByParent(true);
                    keeper->setChildMouseEventFilter(true);
                    outputTouchDeliverLog(this, target, event, "NQItem::deliverTouchEvent for childMouseEventFilter mouse");
                    keepLastTouchEvent(event);
                    return true;
                }
            }
            
            target = target->parentItem();
        }
#endif

    {
            // Deliver the touch event to the focus item
            QQuickItemPrivate *targetPrivate = QQuickItemPrivate::get(this);
            transformTouchPoints(const_cast<QList<QTouchEvent::TouchPoint>&>(event->touchPoints()), this);
            NQItem *nqtarget = qobject_cast<NQItem*>(this);
            // touch point extend data must be updated before sending touch event to item.
            keeper->updateTouchPointExtendData(touch);
            if (nqtarget) {
                QCoreApplication::sendEvent(nqtarget->getPadEventHandler()? nqtarget->getPadEventHandler():nqtarget, event);
            }
            else {
                QCoreApplication::sendEvent(this, event);
            }
        
            if (event->isAccepted()) {    
                keeper->setReceiver(this);
                outputTouchDeliverLog(this, this, event, "NQItem::deliverTouchEvent to the focus item");
                keepLastTouchEvent(event);
                return true;
            }
    }

#if 0
        // If the touch event wasn't accepted, synthesize a mouse event and see if the item wants it.
        QQuickItemPrivate *itemPrivate = QQuickItemPrivate::get(target);
        if (itemPrivate->acceptedMouseButtons() & Qt::LeftButton) {
            //  send mouse event
            event->setAccepted(winPrivate->translateTouchToMouse(target, event));
            if (event->isAccepted()) {
                m_padEventReceiverListener->setReceiver(target);
                keepLastTouchEvent(event);
                outputTouchDeliverLog(this, target, event, "NQItem::deliverTouchEvent to the focus item for mouse");
                return true;
            }
        }
#endif
        delete event;
    }

#ifdef NQTOUCH_NGLOG_OUTPUT
    printf( "NQItem::deliverTouchEvent no receiver!!!");
#endif

    return false;
}