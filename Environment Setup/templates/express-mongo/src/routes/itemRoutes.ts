import express from 'express'
import {
	getItems,
	getItem,
	createItem,
	updateItem,
	deleteItem,
} from '../controllers/itemController'

const router = express.Router()

router.route('/').get(getItems).post(createItem)

router.route('/:id').get(getItem).put(updateItem).delete(deleteItem)

export default router
