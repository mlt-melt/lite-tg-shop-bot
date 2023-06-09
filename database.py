import sqlite3
import threading
import os
import time

lock = threading.Lock()

class DB:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.connection.isolation_level = None


    def add_user(self, user_id, username):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result == None:
                    self.cursor.execute('INSERT INTO users (user_id, username, status, pay_count) VALUES (?, ?, ?, ?)', (user_id, username, 'reg', 0))
                    return
                else:
                    return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_users(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, user_id FROM users ORDER BY id ASC')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_goods(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM goods')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_instances(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM goodsInstances')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_good_instances(self, goodId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM goodsInstances WHERE goodId=? AND status!="sold"', (goodId,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    
    def check_userstat(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result == None:
                    return None
                else:
                    return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def get_rules(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT text FROM rules')
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def change_status(self, user_id, status):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET status=? WHERE user_id=?', (status, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def check_ban(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == 'ban':
                    return False
                else:
                    return True
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def get_all_faq(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM faq')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_usernamerev(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT username FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_user_pay_count(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT pay_count FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == None:
                    return 0
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_user_pay_sum(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT SUM(price) FROM orders WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_user_status(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_cat(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM categories')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_subcat(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM subcategories WHERE categoryid=?', (catid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_goods_user(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name, description, price, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_cat_id_by_subcat_id(self, subcatId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT categoryid FROM subcategories WHERE id=?', (subcatId,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_goodinfo(self, goodid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute(f'SELECT name, description, price, photo FROM goods WHERE id=?', (goodid,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_promos(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name, percent, activations, actLimit FROM promo')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_promo(self, name, percent, actLimit):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO promo (name, percent, actLimit, activations) VALUES (?, ?, ?, ?)', (name, percent, actLimit, "0"))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_promo(self, promoName=None, promoId=None):
        with self.connection:
            try:
                lock.acquire(True)
                if promoName != None:
                    self.cursor.execute('DELETE FROM promo WHERE name=?', (promoName,))
                else:
                    self.cursor.execute('DELETE FROM promo WHERE id=?', (promoId,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_promo_info(self, promo):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, percent, actLimit, activations FROM promo WHERE name=?', (str(promo),))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_promo_info_by_id(self, promoId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name, percent, activations, actLimit FROM promo WHERE id=?', (promoId,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_promo_from_order(self, orderId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT promo FROM orders WHERE id=?', (orderId,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def use_promo(self, promo):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT actLimit, activations FROM promo WHERE name=?', (promo,))
                result = self.cursor.fetchone()
                if int(result[0]) <= int(result[1]) + 1:
                    self.cursor.execute('DELETE FROM promo WHERE name=?', (promo,))
                else:
                    self.cursor.execute('UPDATE promo SET activations=activations+1 WHERE name=?', (promo,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_order(self, user_id, goodId, promo, price):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO orders (user_id, status, goodId, promo, price, time_of_creating, paymentLink) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, 'created', goodId, promo, price, time.time(), ""))
                self.cursor.execute('SELECT id FROM orders WHERE user_id=? ORDER BY id DESC LIMIT 1', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_orders(self, timeStamp):
        with self.connection:
            try:
                lock.acquire(True)
                if timeStamp == "all":
                    timeS = int(time.time())
                elif timeStamp == "today":
                    timeS = 86400
                elif timeStamp == "week":
                    timeS = 604800
                elif timeStamp == "month":
                    timeS = 2678400
                self.cursor.execute('SELECT id FROM orders WHERE time_of_creating>? AND status=?', ((int(time.time()) - timeS), "paid"))
                result1 = self.cursor.fetchall()
                self.cursor.execute('SELECT SUM(price) FROM orders WHERE time_of_creating>? AND status=?', ((int(time.time()) - timeS), "paid"))
                result2 = self.cursor.fetchall()
                return [result1, result2[0][0]]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def remove_old_orders(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM orders WHERE time_of_creating<? AND status=?', ((int(time.time()) - 3600), "created"))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def upd_payment_link(self, order_id, paymentLink):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET paymentLink=? WHERE id=?', (paymentLink, order_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_payment_link(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT paymentLink FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def upd_msg_reply_id(self, order_id, msgId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET msgId=? WHERE id=?', (msgId, order_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_msg_reply_id(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT msgId FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def pay_order(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET status=? WHERE id=?', ('paid', order_id))
                self.cursor.execute('SELECT user_id FROM orders WHERE id=?', (order_id,))
                usr = self.cursor.fetchone()
                self.cursor.execute('UPDATE users SET pays=?, pay_count=pay_count+1 WHERE user_id=?', ('yes', usr[0]))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def add_good_instance(self, goodId, fileName, description):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO goodsInstances (goodId, fileName, description, status) VALUES (?, ?, ?, ?)', (goodId, fileName, description, "new"))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def give_good_instance(self, goodId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, fileName, description FROM goodsInstances WHERE goodId=? ORDER BY id DESC LIMIT 1', (goodId,))
                goodIsinstance = self.cursor.fetchone()
                self.cursor.execute('UPDATE goodsInstances SET status=? WHERE id=?', ('sold', goodIsinstance[0]))
                self.cursor.execute('DELETE FROM goodsInstances WHERE id=?', (goodIsinstance[0],))
                return goodIsinstance
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_good_for_order(self, orderId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT goodId FROM orders WHERE id=?', (orderId,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_wait_order(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM orders WHERE user_id=? AND status=?', (user_id, "created"))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_token(self, paym):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT token FROM payments WHERE name=?', (paym,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def ban_user(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET status=? WHERE user_id=?', ('ban', user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def unban_user(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET status=? WHERE user_id=?', ('ok', user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changetoken(self, paym, token):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE payments SET token=? WHERE name=?', (token, paym))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def get_all_faq_adm(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM faq')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_faq(self, name, text, photo):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO faq (name, text, photo) VALUES (?, ?, ?)', (name, text, photo))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_faq(self, faqid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name, text, photo FROM faq WHERE id=?', (faqid,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changefaq_name(self, faqid, name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE faq SET name=? WHERE id=?', (name, faqid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changefaq_text(self, faqid, text):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE faq SET text=? WHERE id=?', (text, faqid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_faq(self, faqid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM faq WHERE id=?', (faqid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def get_all_cat_adm(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM categories')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_cat(self, name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO categories (name) VALUES (?)', (name, ))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_subcat_adm(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM subcategories WHERE categoryid=?', (catid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_subcat(self, catid, name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO subcategories (categoryid, name) VALUES (?, ?)', (catid, name))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_goods(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM goods WHERE subcategoryid=?', (subcatid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_cat_name(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM categories WHERE id=?', (catid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_subcat_name(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM subcategories WHERE id=?', (subcatid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changename_cat(self, catid, name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE categories SET name=? WHERE id=?', (name, catid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changename_subcat(self, subcatid, name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE subcategories SET name=? WHERE id=?', (name, subcatid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_good(self, subcatid, name, description, photo, price):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO goods (subcategoryid, name, description, price, photo) VALUES (?, ?, ?, ?, ?)', (subcatid, name, description, price, photo))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_namegood(self, goodid, name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE goods SET name=? WHERE id=?', (name, goodid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_descgood(self, goodid, desc):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE goods SET description=? WHERE id=?', (desc, goodid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_pricegood(self, goodid, price):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE goods SET price=? WHERE id=?', (price, goodid))
                return
            except Exception as ex:
                print(ex)
                self.connection.rollback()
            finally:
                lock.release()

    def del_good(self, goodid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT photo FROM goods WHERE id=?', (goodid,))
                result = self.cursor.fetchone()
                if result[0] == 'None':
                    self.cursor.execute('DELETE FROM goods WHERE id=?', (goodid,))
                else:
                    try:
                        os.remove(f'{os.getcwd()}/images/{result[0]}')
                    except:
                        pass
                    self.cursor.execute('DELETE FROM goods WHERE id=?', (goodid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_namecat(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM categories WHERE id=?', (catid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_cat(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM subcategories WHERE categoryid=?', (catid,))
                result = self.cursor.fetchall()
                for i in result:
                    self.cursor.execute('DELETE FROM goods WHERE subcategoryid=?', (i[0],))
                self.cursor.execute('DELETE FROM subcategories WHERE categoryid=?', (catid,))
                self.cursor.execute('DELETE FROM categories WHERE id=?', (catid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_namesubcat(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM subcategories WHERE id=?', (subcatid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_subcat(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM goods WHERE subcategoryid=?', (subcatid,))
                self.cursor.execute('DELETE FROM subcategories WHERE id=?', (subcatid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def check_goods(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM goods WHERE subcategoryid=?', (subcatid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_order_info(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id, goodId FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changerules(self, rules):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE rules SET text=?', (rules,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def del_all_instances(self, goodId):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT fileName FROM goodsInstances WHERE goodId=?', (goodId,))
                result = self.cursor.fetchall()
                self.cursor.execute('DELETE FROM goodsInstances WHERE goodId=?', (goodId,))
                for filename in result:
                    os.remove(f'{os.getcwd()}/files/goodsInstancesFiles/{filename}')
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_user_info(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT username, pay_count FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    